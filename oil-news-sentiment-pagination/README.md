# Crude Oil Headline Scraper

This repository contains a Python-based utility for programmatically retrieving historical news headlines for crude oil (Topic: CRU) using the **LSEG (London Stock Exchange Group) Data Library**.

## Overview
The script is designed to build a robust dataset of market-moving headlines to support volatility modeling and financial analysis (such as GARCH-based forecasting). It automates the collection of English-language headlines and exports them into a structured CSV format.

## Implementation Details

### The Motivation for Pagination
During development, I found that the LSEG API performance was non-linear regarding the `count` parameter. Requesting large volumes of data in a single call (e.g., increasing the headline count from 5,000 to 10,000) caused the API to become **exponentially slower** and frequently triggered timeout errors.

To solve this, I implemented a pagination strategy to ensure script stability and efficiency.

### Pagination Strategy
The script uses a `while` loop to "walk" backward through time in manageable increments:
* **Batching:** Headlines are requested in batches of 500. This size optimizes server response time and prevents the session from timing out.
* **Dynamic Date Anchoring:** After each request, the script identifies the oldest headline in the current batch and reassigns its timestamp as the `END` point for the next iteration.
* **Performance:** Collected batches are stored in a Python list, which is more computationally efficient for iterative appending than a DataFrame, before being concatenated and deduplicated at the end.

## Limitations
Users should be aware that the **LSEG Data Library imposes a hard cap of 15 months** of historical headlines for this specific endpoint. Regardless of the `STOP_DATE` set in the script, the API will not return data older than this 15-month window.

## Usage
The script outputs a file named `crude_oil_headlines_raw.csv`, containing the concatenated results and a timestamp log of the retrieval process.
