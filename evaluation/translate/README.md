## Chrome Translation Evaluation

The script in `index.js` translates the phrase "I can understand the words used
by my grandfather and like coffee." for the majority of languages supported by
Google Translate. It generates `index.html` and `translations.json`.

Running this script on the page `index.html` shows that most translations have a
unique width. The concrete uniqueness will depend on the system and fonts that
are used, but can be fine tuned to fit every system.

```js
let p_tags = document.querySelectorAll("p");
let widths = [];
let width_to_text = {};
p_tags.forEach((p) => {
  let width = p.getBoundingClientRect().width;
  widths.push(width);
  if (!width_to_text[width]) width_to_text[width] = [];
  width_to_text[width].push({
    id: p.id,
    text: p.innerText,
  });
});
console.log(widths);
console.log(`Total Widths: ${widths.length}`);
console.log(`Unique Widths: ${new Set(widths).size}`);

console.log("Duplicates:");
for (let width in width_to_text) {
  if (width_to_text[width].length > 1) console.log(width, width_to_text[width]);
}
```

**Output using Chrome 126 on macOS Sonoma 14.5:**

```
[
    469.66796875,
    410.341796875,
    436.796875,
    320.46875,
    639.23828125,
    347.705078125,
    542.87109375,
    450.9765625,
    403.92578125,
    373.154296875,
    453.720703125,
    417.744140625,
    386.416015625,
    360.810546875,
    436.7578125,
    398.505859375,
    486.11328125,
    272.001953125,
    272.001953125,
    404.228515625,
    365.2734375,
    383.916015625,
    412.939453125,
    325.068359375,
    400.48828125,
    548.291015625,
    430.673828125,
    409.677734375,
    394.4140625,
    397.626953125,
    471.46484375,
    324.8046875,
    482.05078125,
    423.4375,
    435.390625,
    509.365234375,
    558.3203125,
    702.48046875,
    334.0625,
    280.83984375,
    360.33203125,
    606.6796875,
    310.419921875,
    418.59375,
    496.3671875,
    364.7265625,
    356.416015625,
    347.03125,
    477.65625,
    511.396484375,
    447.3046875,
    391.1328125,
    512.001953125,
    462.578125,
    453.173828125,
    356.1328125,
    346.15234375,
    414.990234375,
    352.578125,
    395.64453125,
    393.203125,
    463.84765625,
    274.912109375,
    473.291015625,
    330.80078125,
    376.81640625,
    374.1015625,
    522.28515625,
    407.91015625,
    551.767578125,
    423.45703125,
    516.494140625,
    509.3359375,
    350.771484375,
    530.9375,
    649.2578125,
    389.658203125,
    549.140625,
    372.0703125,
    366.328125,
    294.19921875,
    377.3046875,
    437.36328125,
    607.890625,
    359.921875,
    611.103515625,
    435.634765625,
    405.56640625,
    368.3203125,
    436.728515625,
    323.046875,
    505.64453125,
    382.96875,
    433.759765625,
    528.22265625,
    392.041015625,
    594.6875,
    483.896484375,
    393.974609375,
    496.34765625,
    483.017578125,
    415.15625,
    347.578125,
    370.1171875,
    429.658203125,
    466.953125,
    438.06640625,
    423.8671875,
    479.814453125,
    394.248046875,
    471.46484375,
    577.03125,
    644.765625,
    428.92578125,
    506.8359375,
    316.396484375,
    338.90625,
    571.875,
    437.666015625,
    412.783203125,
    428.017578125,
    420.322265625,
    381.123046875,
    320.21484375,
    427.2265625,
    431.2890625,
    389.1796875,
    527.6171875,
    444.16015625,
    270.625,
    522.5390625
]
Total Widths: 131
Unique Widths: 129
Duplicates:
[
    {
        "id": "zh-CN",
        "text": "我能理解祖父使用的单词和喜欢咖啡。"
    },
    {
        "id": "zh-TW",
        "text": "我能理解祖父使用的單詞和喜歡咖啡。"
    }
]
[
    {
        "id": "fil",
        "text": "Naiintindihan ko ang mga salitang ginamit ng aking lolo at tulad ng kape."
    },
    {
        "id": "tl",
        "text": "Naiintindihan ko ang mga salitang ginamit ng aking lolo at tulad ng kape."
    }
]
```

On this system, there are only two widths that are repeating. The first is
Simplified vs. Traditional Chinese. Here, all fonts are monospaced and only the
visual of a character differs, never the amount of characters. The two can,
however, be easily differentiated using the `unicode-range` feature of
`@font-face` which effectively allows charset detection. The second is Filipino
and Tagalog, which the API does not seem to differentiate. Note that Filipino is
["Tagalog-based"](https://en.wikipedia.org/wiki/Filipino_language#Comparison_of_Filipino_and_Tagalog).
