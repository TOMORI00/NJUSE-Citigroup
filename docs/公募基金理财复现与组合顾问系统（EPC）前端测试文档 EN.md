# Front End Test Document of Mutual fund/financial management reapperence and advisory  portfolio system(EPC)

## 1. Introduction

### 1.1 Purpose

The purpose of this document is to describe whether the final mutual fund/financial management reapperence and advisory  portfolio system meets all of the functional requirements listed in the requirements specification and summarize the deficiency in the development process.

## 2. Scope of Testing

The final public fund analysis and recommendation system has a login screen, a user type selection screen, a professional user interface and a ordinary user interface.

The front-end test document focuses on the switching between different user interfaces and the testing results of function points in the user interface.

The function points contained in different interfaces are shown in the following table.

| Interface                     | Function Points                                              |
| ----------------------------- | ------------------------------------------------------------ |
| User Login Interface          | None                                                         |
| User type selection interface | Download analysis document                                   |
| Professional User Interface   | 1. Uploading Investment History<br/>2. User Investment History Recurrence<br/>3. Comparison Recurrence<br/>4. Portfolio Recommendations<br>5. Using customer tracing blank |
| Ordinary User Interface       | Portfolio Recommendations                                    |

## 3. Testing Results

### 3.1 Testing of interface display and switching

```
     - Login Screen
     - User Type Selection Screen
     - Professional User Interface
         - Investment suggestion tab-pane
         - Investment recurrence tab-pane
         - User tracing blank tab-pane
     - Ordinary User Interface
         - Current recommendation tab-pane
         - History recommendation tab-pane
```

### 3.2 Testing of function points

The following table shows the test results for different function points.

| Function Point                     | Input                                                        | Expected Results                                             | Test Result |
| ---------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ----------- |
| Download Analysis File             | None                                                         | Successfully download analysis file to local disk.           | PASSED      |
| Uploading Investment History       | 1. No document uploaded<br>2. Upload document in incorrect format | 1. Prompt no document uploaded<br>2. Prompt document format error | PASSED      |
| User Investment History Recurrence | None                                                         | Line chart showing user investment history                   | PASSED      |
| Comparison Recurrence              | Select high, medium and low risk level                       | Line chart showing the profits under certain risk level      | PASSED      |
| Portfolio Recommendations          | Select high, medium and low risk level                       | Provide portfolio recommendations under certain risk level.  | PASSED      |
| Using customer tracing blank       | add、delete、edit、search customer info and customer communicate info | record info correctly                                        | PASSED      |