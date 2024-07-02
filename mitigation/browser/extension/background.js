browser.webRequest.onBeforeRequest.addListener(
  (details) => {
    let filter = browser.webRequest.filterResponseData(details.requestId);
    let decoder = new TextDecoder("utf-8");

    filter.ondata = (event) => {
      let str = decoder.decode(event.data, { stream: true });

      if (details.type == "stylesheet") {
        const regex = new RegExp(
          "url\\(.*?\\)|image\\(.*?\\)|image-set\\(.*?\\)",
          "gm"
        );
        let matches = str.match(regex);
        if (matches)
          for (let match of matches) {
            match = match.replaceAll("'", "");
            match = match.replaceAll('"', "");
            match = match.replace(/\s\d+x/g, "");
            match = match.replace(/\s\d+x/g, "");
            match = match.replace(/\s\d+x/g, "");
            match = match.replaceAll("image-set(", "");
            match = match.replaceAll("image(", "");
            match = match.replaceAll("url(", "");
            match = match.replaceAll(")", "");
            match = match.replace(/type\(.*\)/g, "");

            if (match.startsWith("data:")) continue;
            for (let url of match.split(","))
              browser.tabs
                .query({ active: true, currentWindow: true })
                .then((tabs) => {
                  browser.tabs.sendMessage(tabs[0].id, {
                    command: "fetch",
                    url: url,
                  });
                });
          }
      }
      filter.write(event.data);
      filter.disconnect();
    };
  },
  { urls: ["<all_urls>"] },
  ["blocking"]
);
