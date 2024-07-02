// three languages are commented out because the API responded with error codes for them
var langs = {
    af: "Afrikaans",
    sq: "Albanian",
    am: "Amharic",
    ar: "Arabic",
    hy: "Armenian",
    as: "Assamese",
    ay: "Aymara",
    az: "Azerbaijani",
    bm: "Bambara",
    eu: "Basque",
    be: "Belarusian",
    bn: "Bengali",
    bho: "Bhojpuri",
    bs: "Bosnian",
    bg: "Bulgarian",
    ca: "Catalan",
    ceb: "Cebuano",
    "zh-CN": "Chinese Simplified",
    "zh-TW": "Chinese Traditional",
    co: "Corsican",
    hr: "Croatian",
    cs: "Czech",
    da: "Danish",
    dv: "Dhivehi",
    doi: "Dogri",
    nl: "Dutch",
    en: "English",
    eo: "Esperanto",
    et: "Estonian",
    ee: "Ewe",
    fil: "Filipino",
    fi: "Finnish",
    fr: "French",
    fy: "Frisian",
    gl: "Galician",
    ka: "Georgian",
    de: "German",
    el: "Greek",
    gn: "Guarani",
    gu: "Gujarati",
    // ht: "Haitian Creole",
    ha: "Hausa",
    haw: "Hawaiian",
    he: "Hebrew",
    hi: "Hindi",
    hmn: "Hmong",
    hu: "Hungarian",
    is: "Icelandic",
    ig: "Igbo",
    ilo: "Ilokano",
    id: "Indonesian",
    ga: "Irish",
    it: "Italian",
    ja: "Japanese",
    jv: "Javanese",
    kn: "Kannada",
    kk: "Kazakh",
    km: "Khmer",
    rw: "Kinyarwanda",
    gom: "Konkani",
    ko: "Korean",
    kri: "Krio",
    ku: "Kurdisch",
    ckb: "Kurdisch (Sorani)",
    ky: "Kirgisisch",
    lo: "Lao",
    la: "Latein",
    lv: "Lettisch",
    ln: "Lingala",
    lt: "Litauisch",
    lg: "Luganda",
    lb: "Luxemburgisch",
    mk: "Mazedonisch",
    mai: "Maithili",
    mg: "Malagasy",
    ms: "Malay",
    ml: "Malayalam",
    mt: "Maltesisch",
    mi: "Maori",
    mr: "Marathi",
    // mni: "Meitei (Manipuri)",
    // lus: "Mizo",
    mn: "Mongolisch",
    my: "Myanmar (Birmanisch)",
    ne: "Nepalesisch",
    no: "Norwegisch",
    ny: "Nyanja (Chichewa)",
    or: "Odia (Oriya)",
    om: "Oromo",
    ps: "Paschtunisch",
    fa: "Persisch",
    pl: "Polnisch",
    pt: "Portugiesisch (Portugal, Brasilien)",
    pa: "Panjabi",
    qu: "Quechua",
    ro: "Rumänisch",
    ru: "Russisch",
    sm: "Samoanisch",
    sa: "Sanskrit",
    gd: "Schottisches Gälisch",
    nso: "Sepedi",
    sr: "Serbisch",
    st: "Sesotho",
    sn: "Shona",
    sd: "Sindhi",
    si: "Singhalesisch",
    sk: "Slowakisch",
    sl: "Slowenisch",
    so: "Somali",
    es: "Spanisch",
    su: "Sundanesisch",
    sw: "Swahili",
    sv: "Schwedisch",
    tl: "Tagalog (Philippinisch)",
    tg: "Tadschikisch",
    ta: "Tamil",
    tt: "Tatarisch",
    te: "Telugu",
    th: "Thai",
    ti: "Tigrinya",
    ts: "Tsonga",
    tr: "Türkisch",
    tk: "Turkmenisch",
    ak: "Twi (Akan)",
    uk: "Ukrainisch",
    ur: "Urdu",
    ug: "Uigurisch",
    uz: "Usbekisch",
    vi: "Vietnamesisch",
    cy: "Walisisch",
    xh: "Xhosa",
    yi: "Jiddisch",
    yo: "Yoruba",
    zu: "Zulu",
};

import { GoogleTranslator } from "@translate-tools/core/translators/GoogleTranslator/index.js";
import fs from "fs";

async function main() {
    const phrase = "I can understand the words used by my grandfather and like coffee.";

    const translator = new GoogleTranslator({
        headers: {
          "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
        },
      });
      
      let output = {};
      let html_output = "<html><head><title>Translations</title><style>p {width: fit-content;}</style></head><body>";
      
      for (let lang in langs) {
        console.log(lang, langs[lang]);
        let translation = await translator.translate(phrase, "en", lang);
        console.log(langs[lang], translation);
        output[lang] = translation;
        html_output += `<p id="${lang}">${translation}</p>`;
      }
      html_output += "</body></html>";
      
      console.log(output);
      fs.writeFileSync("translations.json", JSON.stringify(output));
      fs.writeFileSync("index.html", html_output);
}

main();