# MediBlok

Secure Medical Reports Storage using Blockchain

## Description

We have built a blockchain-based web app 'MediBlok' that helps doctors store the medical reports of the patients in a secure manner. We have implemented the 'Proof of Work' consensus algorithm.

A doctor can create a medical report by clicking on Add Report and filling in the required information. He can also view his reports by clicking on View Report.

## Zero Knowledge Proof

We have implemented the 'Zero-Knowledge Proof (ZKP)' algorithm to verify the transactions. We are using reportID, which is the combination of the Medical Report and Password of the logged-in doctor to verify the transaction.

## how to start:

install requirements

```
$ pip install -r requirements.txt
```

clone and start:

```
$ git clone https://github.com/shubhpriyadarshi/Crypto-Blockchain-Assignment.git
$ cd Crypto-Blockchain-Assignment
$ pipenv install
$ pipenv shell
$ python main.py
```

#### Sample Users:

-   ayush : ayush-mediblok

## Contributors

-   Ayush Sunil Pote : 2019A7PS0112H
-   Shubh Priyadarshi : 2019A7PS0100H
-   Piyush Lalwani : 2019A7PS0081H
