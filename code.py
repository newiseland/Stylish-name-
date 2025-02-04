function stylizeName(name) {
  let stylizedNames = [];

  // 1. Capitalization Variations
  stylizedNames.push(name.toUpperCase());
  stylizedNames.push(name.toLowerCase());
  stylizedNames.push(name.split('').map((char, i) => i % 2 === 0 ? char.toUpperCase() : char.toLowerCase()).join('')); // Alternating case

  // 2. Embellishments
  stylizedNames.push(`*${name}*`);
  stylizedNames.push(`_${name}_`);
  stylizedNames.push(`~${name}~`);
  stylizedNames.push(`.${name}.`);
  stylizedNames.push(`-${name}-`);

  // 3.  "Fancy" Text (using a limited set of Unicode characters - this is the trickiest part)
  const fancyChars = {
    'a': '𝔞', 'b': '𝔟', 'c': '𝔠', 'd': '𝔡', 'e': '𝔢', 'f': '𝔣', 'g': '𝔤', 'h': '𝔥', 'i': '𝔦', 'j': '𝔧', 'k': '𝔨', 'l': '𝔩', 'm': '𝔪',
    'n': '𝔫', 'o': '𝔬', 'p': '𝔭', 'q': '𝔮', 'r': '𝔯', 's': '𝔰', 't': '𝔱', 'u': '𝔲', 'v': '𝔳', 'w': '𝔴', 'x': '𝔵', 'y': '𝔶', 'z': '𝔷',
    'A': '𝔄', 'B': '𝔅', 'C': 'ℭ', 'D': '𝔇', 'E': '𝔈', 'F': '𝔉', 'G': '𝔊', 'H': 'ℌ', 'I': 'ℑ', 'J': '𝔍', 'K': '𝔎', 'L': '𝔏', 'M': '𝔐',
    'N': '𝔍', 'O': '𝔒', 'P': '𝔓', 'Q': '𝔔', 'R': 'ℜ', 'S': '𝔖', 'T': '𝔗', 'U': '𝔘', 'V': '𝔙', 'W': '𝔚', 'X': '𝔛', 'Y': '𝔜', 'Z': '𝔛'
  };

  let fancyName = "";
  for (let i = 0; i < name.length; i++) {
    fancyName += fancyChars[name[i]] || name[i]; // Use fancy char if available, otherwise use original
  }
  stylizedNames.push(fancyName);



  return stylizedNames;
}


// Example Usage (This part will be WITHIN your Bots.business code block/webhook)
let userName = /* Get the user's input from Bots.business (How you do this depends on Bots.business) */ "John"; // Example
let styledNames = stylizeName(userName);

// Now 'styledNames' is an array.  You need to send this back to the user in Bots.business.
// How you display this array (e.g., list, carousel) is also specific to Bots.business.
console.log(styledNames); // For debugging in your Bots.business code block

// Example of how you might format the output string for the user
let outputString = "Here are some stylized versions of your name:\n\n";
styledNames.forEach(name => outputString += name + "\n");

// Use Bots.business's "send message" function to display 'outputString' to the user.
      
