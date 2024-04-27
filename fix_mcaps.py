import sys
from mcap.writer import Writer
from mcap.reader import make_reader

def fix_mcap_file(input_file_path, output_file_path):
    with open(input_file_path, "rb") as input_file:
        reader = make_reader(input_file)

        with open(output_file_path, "wb") as output_file:
            writer = Writer(output_file)

            # Iterate through all schemas and channels in the original file
            for schema in reader.schemas.values():
                writer.register_schema(schema.name, schema.encoding, schema.data)

            for channel in reader.channels.values():
                writer.register_channel(channel.id, channel.topic, channel.message_encoding, channel.schema_id)

            # Reading and writing all messages
            for message in reader.read_messages():
                writer.add_message(
                    log_time=message.log_time,
                    publish_time=message.publish_time,
                    channel_id=message.channel_id,
                    data=message.data
                )

            print(f"Processed and copied messages to {output_file_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_input_mcap>")
    else:
        input_file_path = sys.argv[1]
        output_file_path = sys.argv[1] + "_fixed"
        fix_mcap_file(input_file_path, output_file_path)
