import tensorflow as tf
from datasets import load_dataset
from transformers import DistilBertTokenizerFast, TFDistilBertForQuestionAnswering, create_optimizer

# Load SQuAD dataset
dataset = load_dataset('squad')

# Use the fast tokenizer
tokenizer = DistilBertTokenizerFast.from_pretrained('distilbert-base-uncased')
model = TFDistilBertForQuestionAnswering.from_pretrained('distilbert-base-uncased')


def preprocess_data(examples):
    questions = [q.strip() for q in examples['question']]
    inputs = tokenizer(
        questions,
        examples['context'],
        max_length=384,
        truncation="only_second",
        padding="max_length",
        return_offsets_mapping=True,
        return_tensors='tf'
    )

    offset_mapping = inputs.pop("offset_mapping")
    answers = examples['answers']

    start_positions = []
    end_positions = []

    for i, offset in enumerate(offset_mapping):
        answer = answers[i]
        start_char = answer['answer_start'][0]
        end_char = start_char + len(answer['text'][0])

        sequence_ids = inputs.sequence_ids(i)
        context_start = sequence_ids.index(1)
        context_end = len(sequence_ids) - 1 - sequence_ids[::-1].index(1)

        if offset[context_start][0] > end_char or offset[context_end][1] < start_char:
            start_positions.append(0)
            end_positions.append(0)
        else:
            start_positions.append(
                next(idx for idx, map in enumerate(offset) if map[0] <= start_char and map[1] > start_char))
            end_positions.append(
                next(idx for idx, map in enumerate(offset) if map[0] < end_char and map[1] >= end_char))

    inputs['start_positions'] = tf.convert_to_tensor(start_positions, dtype=tf.int32)
    inputs['end_positions'] = tf.convert_to_tensor(end_positions, dtype=tf.int32)

    return inputs


# Preprocess the dataset and take a subset of 10,000 samples
train_dataset = dataset['train'].select(range(10000)).map(preprocess_data, batched=True,
                                                          remove_columns=dataset['train'].column_names)
eval_dataset = dataset['validation'].select(range(10000)).map(preprocess_data, batched=True,
                                                              remove_columns=dataset['validation'].column_names)


# Convert datasets to TensorFlow datasets
def to_tf_dataset(dataset, batch_size=16):
    def gen():
        for i in range(len(dataset)):
            item = {k: tf.convert_to_tensor(v) for k, v in dataset[i].items()}
            yield item

    return tf.data.Dataset.from_generator(gen,
                                          output_signature={k: tf.TensorSpec(shape=(None,), dtype=tf.int32) for k in
                                                            dataset.features.keys()})


train_tf_dataset = to_tf_dataset(train_dataset).shuffle(1000).batch(16)
eval_tf_dataset = to_tf_dataset(eval_dataset).batch(16)

# Define optimizer, loss, and metrics
batch_size = 16
num_train_steps = len(train_dataset) // batch_size * 3  # num_train_steps = num_batches_per_epoch * num_epochs
optimizer, schedule = create_optimizer(init_lr=3e-5, num_warmup_steps=0, num_train_steps=num_train_steps)

model.compile(optimizer=optimizer, loss=model.compute_loss)  # Model will use its own compute_loss method

# Train the model
model.fit(train_tf_dataset,
          epochs=3,
          validation_data=eval_tf_dataset)

# Evaluate the model
eval_results = model.evaluate(eval_tf_dataset)
print(f"Evaluation results: {eval_results}")

# Save the fine-tuned model and tokenizer
model.save_pretrained("./fine_tuned_distilbert_tf")
tokenizer.save_pretrained("./fine_tuned_distilbert_tf")
