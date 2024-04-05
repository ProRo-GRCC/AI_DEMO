import boto3

# Define a function to split the text into chunks
def split_text(text, max_chunk_size=2900):
    """
    Splits a string into chunks of `max_chunk_size` with respect to word boundaries.
    """
    chunks = []
    while text:
        if len(text) > max_chunk_size:
            # Find the nearest space to the left of the maximum chunk size
            space_index = text.rfind(" ", 0, max_chunk_size)
            if space_index == -1:
                # No spaces found, force split the text
                space_index = max_chunk_size
            chunks.append(text[:space_index])
            text = text[space_index:]  # Remaining text after the space
        else:
            chunks.append(text)
            break
    return chunks

def text_file_to_mp3(filename):
    try:
        # Initialize a boto3 client for Polly
        polly_client = boto3.client('polly')

        # Extract the text from the file
        with open(filename, 'r', encoding='utf-8') as file:
            text = file.read()

        # Split text into chunks
        text_chunks = split_text(text)

        # Define the output MP3 filename based on the input filename
        output_filename = f"{filename.rsplit('.', 1)[0]}.mp3"

        # Process each chunk
        for index, text_chunk in enumerate(text_chunks):
            response = polly_client.synthesize_speech(
                Text=text_chunk,
                OutputFormat='mp3',
                VoiceId='Joanna'
            )
            # Append each audio chunk to the output MP3 file
            if "AudioStream" in response:
                with open(output_filename, "ab") as file:  # Note the 'ab' mode for appending binary data
                    file.write(response['AudioStream'].read())
            else:
                print(f"Could not retrieve audio stream for chunk {index} from Polly response.")

        print(f"MP3 audio file saved as {output_filename}")

    except FileNotFoundError:
        print(f"The file {filename} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        text_file = sys.argv[1]
        text_file_to_mp3(text_file)
    else:
        print("Usage: python text_to_mp3_polly.py <filename>")
