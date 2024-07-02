function fetchURLFromPage(url) {
  console.log("Prefetching: " + url);
  const img = document.createElement("img");
  img.src = url;
  img.style = "display: none;";
  document.documentElement.appendChild(img);
}

browser.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.command === "fetch") {
    fetchURLFromPage(message.url);
  }
});

document.addEventListener("DOMContentLoaded", () => {
  const regex = new RegExp(
    "url\\(.*?\\)|image\\(.*?\\)|image-set\\(.*?\\)",
    "gm"
  );
  const styleTags = document.querySelectorAll("style");
  styleTags.forEach((tag, index) => {
    let matches = tag.innerHTML.match(regex);
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
            fetchURLFromPage(url);
      }
  });
  const styleAttributes = document.querySelectorAll("[style]");
  styleAttributes.forEach((element, index) => {
    let matches = element.getAttribute("style").match(regex);
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
            fetchURLFromPage(url);
      }
  });
});
