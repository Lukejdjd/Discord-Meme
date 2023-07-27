from PIL import Image, ImageDraw, ImageFont, ImageSequence
from moviepy.editor import VideoFileClip
import numpy as np

speech_bubble = Image.open("speechbubble.png").convert("RGBA")

def overlay_speech_bubble_on_image(file_name):
    file_extension = file_name.lower().split(".")[-1]
    output_file_name = f"modified {file_name}"

    if file_extension in ("mp4", "mov"):
        # Process the video file
        clip = VideoFileClip(file_name)
        modified_clip = clip.fl(lambda gf, t: overlay_speech_bubble_on_frame(
            gf(t)
        ))
        modified_clip.write_videofile(
            output_file_name,
            codec="libx264",
            audio=True
        )
        print(f"Video overlay successful. Output: {output_file_name}")
    else:
        # Process the image file
        with Image.open(file_name) as im:
            # Resize the speech bubble once
            speech_bubble_resized = speech_bubble.resize(
                (im.width, im.height // 3),
                resample=Image.LANCZOS
            )

            if im.format == "GIF":
                # Process each frame of the GIF image
                frames = []
                for frame in ImageSequence.Iterator(im):
                    frame = frame.convert("RGBA")
                    frame.paste(speech_bubble_resized, (0, 0), speech_bubble_resized)
                    frames.append(frame)

                # Save the modified GIF
                frames[0].save(
                    output_file_name,
                    save_all=True,
                    append_images=frames[1:],
                    duration=im.info.get("duration", 0),
                    loop=0
                )
                print(f"Image overlay successful. Output: {output_file_name}")
            else:
                # Overlay the speech bubble on the image
                im.paste(speech_bubble_resized, (0, 0), speech_bubble_resized)

                # Save the modified image
                im.save(output_file_name)
                print(f"Image overlay successful. Output: {output_file_name}")

def overlay_speech_bubble_on_frame(frame):
    # Load and resize the speech bubble
    speech_bubble = Image.open("speechbubble.png").convert("RGBA")
    speech_bubble = speech_bubble.resize(
        (frame.shape[1], frame.shape[0] // 3),
        resample=Image.LANCZOS
    )

    # Overlay the speech bubble on the frame
    frame_pil = Image.fromarray(frame)
    frame_pil.paste(speech_bubble, (0, 0), speech_bubble)

    return np.array(frame_pil)

def overlay_caption_on_image(file_name, caption_text):
    file_extension = file_name.lower().split(".")[-1]
    output_file_name = f"modified {file_name}"

    if file_extension in ("mp4", "mov"):
        # Process the video file
        clip = VideoFileClip(file_name)
        modified_clip = clip.fl(lambda gf, t: overlay_caption_on_frame(
            gf(t), caption_text)
        )
        modified_clip.write_videofile(
            output_file_name,
            codec="libx264",
            audio=True
        )
        print(f"Caption overlay successful. Output: {output_file_name}")
    else:
        with Image.open(file_name) as im:
            if im.format == "GIF":
                # Process each frame of the GIF image
                frames = []
                for frame in ImageSequence.Iterator(im):
                    frame = frame.convert("RGBA")
                    draw = ImageDraw.Draw(frame)

                    # Calculate the rectangle height for the caption box
                    rectangle_height = frame.height // 4
                    draw.rectangle((0, 0, im.width, rectangle_height), fill=(255, 255, 255))

                    # Set the font and position for the caption text
                    font = ImageFont.truetype("caption.otf", rectangle_height // 2)
                    bbox = font.getbbox(caption_text)
                    text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
                    x = (frame.width - text_width) // 2
                    y = (rectangle_height - text_height) // 2

                    # Draw the caption text on the frame
                    draw.text((x, y), caption_text, font=font, fill=(0, 0, 0))

                    frames.append(frame)

                # Save the modified GIF
                frames[0].save(
                    output_file_name,
                    save_all=True,
                    append_images=frames[1:],
                    duration=im.info.get("duration", 0),
                    loop=0
                )
                print(f"Caption overlay successful. Output: {output_file_name}")
            else:
                # Process the image file
                draw = ImageDraw.Draw(im)

                # Calculate the rectangle height for the caption box
                rectangle_height = im.height // 5
                draw.rectangle((0, 0, im.width, rectangle_height), fill=(255, 255, 255))

                # Set the font and position for the caption text
                font = ImageFont.truetype("caption.otf", rectangle_height // 2)
                bbox = font.getbbox(caption_text)
                text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
                x = (im.width - text_width) // 2
                y = (rectangle_height - text_height) // 2

                # Draw the caption text on the image
                draw.text((x, y), caption_text, font=font, fill=(0, 0, 0))

                # Save the modified image
                im.save(output_file_name)
                print(f"Caption overlay successful. Output: {output_file_name}")

def overlay_caption_on_frame(frame, caption_text):
    # Convert the frame to a PIL image
    frame_pil = Image.fromarray(frame)
    draw = ImageDraw.Draw(frame_pil)

    # Calculate the rectangle height for the caption box
    rectangle_height = frame_pil.height // 7
    draw.rectangle((0, 0, frame_pil.width, rectangle_height), fill=(255, 255, 255))

    # Set the font and position for the caption text
    font = ImageFont.truetype("caption.otf", rectangle_height // 2)
    bbox = font.getbbox(caption_text)
    text_size = (bbox[2] - bbox[0], bbox[3] - bbox[1])
    x = (frame_pil.width - text_size[0]) // 2
    y = (rectangle_height - text_size[1]) // 2

    # Draw the caption text on the frame
    draw.text((x, y), caption_text, font=font, fill=(0, 0, 0))

    return np.array(frame_pil)

if __name__ == "__main__":
    overlay_option = int(input("Choose an option (1 for speech bubble overlay, 2 for caption image): "))

    file_name = input("Enter the file name: ")

    if overlay_option == 1:
        overlay_speech_bubble_on_image(file_name)
    elif overlay_option == 2:
        caption_text = str(input("Enter the caption: "))
        overlay_caption_on_image(file_name, caption_text)
    else:
        print("Invalid overlay option.")