from flask import Flask, request, Response
import os

CLIENT_PLACEHOLDER = "XPLACEHOLDERX"
TESTCASE_PLACEHOLDER = "YPLACEHOLDERY"
OUTPUT_FILE = "css-detection.csv"
DELIMITER = ";"
CLIENT_WHITELIST = [
    "web-gmail",
    "web-aol",
    "web-outlook",
    "web-icloud",
    "web-yahoo",
    "web-mailcow",
    "web-roundcube",
    "web-proton",
    "desktop-thunderbird",
    "desktop-outlook",
    "desktop-apple",
    "desktop-winmail",
    "android-gmail",
    "android-outlook",
    "android-samsung",
    "ios-mail",
    "ios-gmail",
    "ios-outlook"
]

app = Flask(__name__)


# format /client-identifier/feature
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):
    print(f"[+] Received request:: {path}")
    ip = request.remote_addr
    if request.environ.get('HTTP_X_FORWARDED_FOR') is not None:
        ip = request.environ['HTTP_X_REAL_IP']
    user_agent = request.headers.get('User-Agent', "")
    print(f"[+] IP: {ip}")
    print(f"[+] User Agent: {user_agent}")
    try:
        client_id, detected_feature = path.strip("/").split("/")
        if client_id not in CLIENT_WHITELIST:
            return f"Invalid client", 400
        if detected_feature.endswith(".css"):
            file_path = os.path.join('external', detected_feature)
            with open(file_path, 'r') as file:
                file_content = file.read()
            file_content = file_content.replace(CLIENT_PLACEHOLDER, client_id)
            return Response(file_content, mimetype='text/css')
        print(f"\t[*] Client ID: {client_id}")
        print(f"\t[*] Detected feature: {detected_feature}")
    except:
        print(f"Ill-formatted path: '{path}'!")
        return f"Fail", 400

    with open(OUTPUT_FILE, "a") as fd:
        line = f"{client_id};{detected_feature}\n"
        fd.write(line)

    return f"Success"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
