---
title: "Configuration"
weight: 1
chapter: true
pre: "<b>1. </b>"
---

# Configuration

On this page we will describe all the configuration options available.

## AWS Profile

By setting the `AWS_PROFILE` environment variable, you can control what profile is used to query the organization.

## Configure the environment ordering

By setting the `ENVIRONMENT_WEIGHT` you have control over the order that the environments are returned. For example, if you have a development, testing, acceptance and a production environment. The alphabetical sorting would be: acceptance, development, production and testing.

But we call it `DTAP` and therefor the: development, testing, acceptance, production order is more logical.

By changing the `ENVIRONMENT_WEIGHT` value you can control the order. It's a comma seperated list, and if the word matches with the environment name it will take the index of the matched word. All non-matching environments are appended.  
