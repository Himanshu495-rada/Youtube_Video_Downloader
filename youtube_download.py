import json
from urllib.parse import parse_qs, unquote
def apply_descrambler(stream_data, key):
    otf_type = "FORMAT_STREAM_TYPE_OTF"

    if key == "url_encoded_fmt_stream_map" and not stream_data.get(
        "url_encoded_fmt_stream_map"
    ):
        formats = json.loads(stream_data["player_response"])["streamingData"]["formats"]
        formats.extend(
            json.loads(stream_data["player_response"])["streamingData"][
                "adaptiveFormats"
            ]
        )
        try:
            stream_data[key] = [
                {
                    "url": format_item["url"],
                    "type": format_item["mimeType"],
                    "quality": format_item["quality"],
                    "itag": format_item["itag"],
                    "bitrate": format_item.get("bitrate"),
                    "is_otf": (format_item.get("type") == otf_type),
                }
                for format_item in formats
            ]
        except KeyError:
            cipher_url = []
            for data in formats:
                cipher = data.get("cipher") or data["signatureCipher"]
                cipher_url.append(parse_qs(cipher))
            stream_data[key] = [
                {
                    "url": cipher_url[i]["url"][0],
                    "s": cipher_url[i]["s"][0],
                    "type": format_item["mimeType"],
                    "quality": format_item["quality"],
                    "itag": format_item["itag"],
                    "bitrate": format_item.get("bitrate"),
                    "is_otf": (format_item.get("type") == otf_type),
                }
                for i, format_item in enumerate(formats)
            ]
    else:
        stream_data[key] = [
            {k: unquote(v) for k, v in parse_qsl(i)}
            for i in stream_data[key].split(",")
        ]

import pytube
pytube.__main__.apply_descrambler = apply_descrambler

url = input('Please enter/paste your youtube link:- ')
yt = pytube.YouTube(url)
stream = yt.streams.all()
a = 0
for i in stream:
    a += 1
    print(a,'] ',i)

video = stream[n-1]
video.download('C:\\Users\\himan\\Downloads')
print('Download is finished')