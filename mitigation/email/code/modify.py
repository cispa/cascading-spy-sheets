from base64 import b64encode
from dataclasses import dataclass
from email.message import Message
from quopri import decodestring
from tempfile import TemporaryFile

from bs4 import BeautifulSoup
from cssutils import parseStyle
from css_inline import inline
from filetype import guess_mime
from requests import get

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"


@dataclass
class DataURL:
    mime_type: str
    encoded: str

    def __repr__(self):
        return f"data:{self.mime_type};base64,{self.encoded}"


def fetch_data_url(url: str) -> DataURL:
    try:
        data = get(url, headers={"User-Agent": USER_AGENT}).content
    except:
        return DataURL("text/plain", "error")
    with TemporaryFile() as file:
        file.write(data)
        mime = guess_mime(file)
    encoded = b64encode(data).decode()
    return DataURL(mime, encoded)


def replace_images(html: str) -> str:
   soup = BeautifulSoup(html, "html.parser")
   for element in soup.descendants:
       if element.name is not None:
           # print(element)
           # src attributes
           if "src" in element.attrs:
               # print(element.attrs["src"])
               if element.attrs["src"].startswith("data:"):
                   continue
               data = fetch_data_url(element.attrs["src"])
               element.attrs["src"] = str(data)
           # background images
           if "style" in element.attrs:
               style = parseStyle(element.attrs["style"])
               if "background-image" not in style:
                   continue
               url = style['background-image']
               url = url.replace('url(', '').replace(')', '')
               data = fetch_data_url(url)
               style['background-image'] = f"url({str(data)})"
               element.attrs['style'] = style.getCssText("")
   return str(soup)


def remove_headers(inp: str) -> str:
    content = inp.split("\n\n", 1)[-1]
    # decodestring does not work if the string is not "Quoted-Printable" encoded (not idempotent)
    if "=3D" in content:
        return decodestring(content.encode("utf-8")).decode()
    return content


def inline_css(inp: str) -> str:
    try:
        inlined = inline(inp)
        return inlined
    except:
        return inp


def clean_html(html: str) -> str:
    # strip the content type, charset, and transfer encoding (otherwise it will be duplicated when replacing the payload)
    content = remove_headers(html)
    replaced_images = replace_images(content)
    css_inlined_payload = inline_css(replaced_images)
    return css_inlined_payload


def modify_email(email: Message) -> Message:
    try:
        for part in email.walk():
            # payload is a list of strings if its a multipart, otherwise it's a string
            if part.is_multipart():
                for payload in part.get_payload():
                    if payload.get_content_type() != "text/html":
                        continue
                    cleaned_payload = clean_html(payload.as_string())
                    payload.set_payload(cleaned_payload)
            elif part.get_content_type() == "text/html":
                part.set_payload(clean_html(part.get_payload()))
    except:
        pass
    return email
