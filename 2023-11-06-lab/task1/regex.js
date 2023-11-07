const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
const phoneRegex = /^\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$/;
const webpageRegex = /^((https|http|ftp)?:\/\/)?(www\.)?([a-zA-Z0-9.-]+\.[a-zA-Z]{2,3})(\/[^\s]*)?$/;

function testRegexExpression(regex, testCases,type) {
    for (const testCase of testCases) {
      const result = regex.test(testCase);
      if (type == "email"){
        if (result){
            console.log("Email - "+ testCase + " is valid")
        }else{
            console.log("Email - "+ testCase + " is invalid")
        }
      }else if(type =="phone"){
        if(result){
            console.log("Phone Number - "+ testCase + " is valid")
        }else{
            console.log("Phone Number - "+ testCase + " is invalid")
        }
      }else{
        if(result){
            console.log("Webpage URL - "+ testCase + " is valid")
        }else{
            console.log("Webpage URL - "+ testCase + " is invalid")
        }
      }
    }
  }

// Email Test Cases
const emailTestCases = [
    "example@example.com",
    "invalid-email",
    "user.name@example.co.uk",
    "user@.com",
    "user123@sub.domain.example123.co",
    "user@123",
    "user@my.domain",
];
console.log("############# Validating Email Test Cases: ###############");
testRegexExpression(emailRegex, emailTestCases,"email");
  
// Phone Number Test Cases
const phoneTestCases = [
    "(123) 456-7890",
    "123-45",
    "555-555-5555",
    "abc-123-defg",
    "1234567890",
    "1-2-3-4-5-6-7-8-9-0",
    "abc-123-defg"
];
  
console.log("\n############# Validating Phone Number Test Cases: #############");
testRegexExpression(phoneRegex, phoneTestCases,"phone");
  
// Webpage URL Test Cases
const webpageTestCases = [
    "http://www.example.com",
    "www.example",
    "https://subdomain.example.co.uk:8080/path/to/page?query=123#section",
    "ftp://.com",
    "ftp://ftp.example.com:8080/path/to/page?query=123#section",
    "https://example.",
    "http://example?.com",
];
  
console.log("\n############# Validating Webpage URL Test Cases: #############");
testRegexExpression(webpageRegex, webpageTestCases,"webpage");