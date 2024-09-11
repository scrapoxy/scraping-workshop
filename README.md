# Fabien's WebScraping Anti-Ban Workshop

![Header](header.jpg)

## Clone the repository

First, clone this repository:

```shell
git clone https://github.com/fabienvauchelles/scraping-workshop.git
cd scraping-workshop
```


## Introduction

Our goal is to understand how anti-bot protections work and how to bypass them.

I created a dedicated website for this workshop [https://trekky-reviews.com](https://trekky-reviews.com).
This website provides a list of hotels for every city, including reviews.

We will collect **name, email and reviews** for each hotel.

During this workshop, we will use the following open-source software:

| Framework                            | Description                                                                  |
|--------------------------------------|------------------------------------------------------------------------------|
| [Scrapy](https://scrapy.org)         | the leading framework for web scraping                                       |
| [Scrapoxy](https://scrapoxy.io)      | the super proxies aggregator                                                 |
| [Playwright](https://playwright.dev) | the latest headless browser framework that integrates seamlessly with Scrapy |
| [Babel.js](https://babeljs.io)       | a transpiler used for deobfuscation purposes                                 |

The scraper can be found at [scrapers/spiders/trekky.py](scrapers/spiders/trekky.py).

All solutions are located in [solutions](solutions).
If you have any difficulties implementing a solution, feel free to copy and paste it. 
However, I recommend taking some time to search and explore to get the most out of the workshop, rather than rushing through it in 10 minutes.

## Requirements

### Operating System

The recommended operating system is **Ubuntu on Linux**, though any Linux distribution or macOS will work.

For Windows users, I recommend either **using WSL2** with Ubuntu or running Ubuntu in a virtual machine.


### Software

Please make sure you have installed the following software:

- Python (version 3 or higher) with virtualenv
- Node.js (version 20 or higher)
- Scrapoxy (with Docker)
- Playwright

If you haven't installed these prerequisites yet, here's some guidance to help you get started:

#### Python

*Linux*

On Linux, I suggest installing Python and its packages using standard package management tools like `python3-pip` for Ubuntu. 

Creating a virtual environment is crucial to avoid mixing with your system's Python installation using this [guide](https://virtualenv.pypa.io/en/latest/user_guide.html).

*Mac*

For Mac users, I recommend installing Python and managing environments through [Anaconda](https://www.anaconda.com/download).

Create a virtual environment inside Anaconda for this workshop.

#### Python libraries

Open a shell and install libraries from `setup.py`:

```shell
pip install -r requirements.txt
```


#### Playwright

After installing the python libraries, run the follow command:

```shell
playwright install
```


#### Node.js

Install Node.js from the [official website](https://nodejs.org/en/download/) or through the version management [NVM](https://github.com/nvm-sh/nvm)


#### Node.js libraries

Open a shell and install libraries from `package.json`:

```shell
npm install
```


#### Scrapoxy

If you already have docker, just run

```shell
docker pull fabienvauchelles/scrapoxy
```

Otherwise, use NPM to install Scrapoxy:

```shell
npm install -g scrapoxy
```


## Challenge 1: Run your first Scraper

The URL to scrape is: [https://trekky-reviews.com/level1](https://trekky-reviews.com/level1)

Our goal is to collect **names, emails, and reviews** for each hotel listed.

Open the file [`scrapers/spiders/trekky.py`](scrapers/spiders/trekky.py).

In Scrapy, a spider is a Python class with a unique `name` property. Here, the name is `trekky`.

The spider class includes a method called `start_requests`, which defines the initial URLs to scrape. 
When a URL is fetched, the Scrapy engine triggers a callback function. 
This callback function handles the parsing of the data. 
It's also possible to generate new requests from within the callback function, allowing for chaining of requests and callbacks.

The structure of items is defined in the file [`scrapers/items.py`](scrapers/items.py). 
Each item type is represented by a dataclass containing fields and a loader:

* `HotelItem`: name, email, review with the loader `HotelItemLoader`
* `ReviewItem`: rating with the loader `ReviewItemLoader`

To run the spider, open a terminal at the project's root directory and run the following command:

```shell
scrapy crawl trekky
```

Scrapy will collect data from **50 hotels**:

```text
2024-07-05 23:11:43 [trekky] INFO: 

We got: 50 items

```

Check the `results.csv` file to confirm that all items were collected.


## Challenge 2: First Anti-Bot protection

The URL to scrape is: [https://trekky-reviews.com/level2](https://trekky-reviews.com/level2)

Update the URL in your scraper to target the new page and execute the spider:

```shell
scrapy crawl trekky
```

Data collection may fail due to **an anti-bot system**.

Pay attention to the **messages** explaining why access is blocked and use this information to correct the scraper.

Hint: It relates to HTTP request headers 😉 

<details>
    <summary>Soluce is here</summary>
    <a href="solutions/challenge-2.py">Open the soluce</a>
</details>


## Challenge 3: Rate limit

The URL to scrape is: [https://trekky-reviews.com/level3](https://trekky-reviews.com/level3)

Update the URL in your scraper to target the new page and execute the spider:

```shell
scrapy crawl trekky
```

Data collection might fail due to **rate limiting** on our IP address.

<table>
    <tr>
        <td>
            <img src="images/warning.png" />
        </td>
        <td>
            Please don't adjust the delay between requests or the number of concurrent requests; <b>that is not our goal</b>. 
            Imagine we need to collect millions of items within a few hours, and delaying our scraping session is not an option. 
            Instead, we will use proxies to distribute requests across multiple IP addresses.
        </td>
    </tr>
</table>

Use [Scrapoxy](https://scrapoxy.io) to bypass the rate limit with a cloud provider (not a proxy service).


### Step 1: Install Scrapoxy

Follow this [guide](https://scrapoxy.io/intro/get-started).


### Step 2: Create a new project

In the new project, deactivate `Intercept HTTPS requests with MITM`:

![Scrapoxy New Project](images/scrapoxy-project-create.png)


### Step 3: Add a Cloud Provider connector

Use [AWS](https://scrapoxy.io/connectors/aws/guide),
[Azure](https://scrapoxy.io/connectors/azure/guide),
[Digital Ocean](https://scrapoxy.io/connectors/digitalocean/guide),
[GCP](https://scrapoxy.io/connectors/gcp/guide) or
[OVH](https://scrapoxy.io/connectors/ovh/guide).

Use **10 proxies** from **a European** region.

![Scrapoxy Connector Create](images/scrapoxy-connector-create.png)

If you don't have an account with these cloud providers, you can create one.

<table>
    <tr>
        <td width="70">
            <img src="images/warning.png" />
        </td>
        <td>
            They typically require a credit card, and you may need to pay a nominal fee of $1 or $2 for this workshop.
            Such charges are common when using proxies. Don't worry; in the next challenge, I'll provide you with free credit.
        </td>
    </tr>
</table>


### Step 4: Install the connector

Cloud Provider requires connector installation:

![Scrapoxy Connector Install](images/scrapoxy-connector-install.png)


### Step 5: Run the connector

![Scrapoxy Connector Run](images/scrapoxy-connector-run.png)


### Step 6: Connect Scrapoxy to the spider

Follow this [guide](https://scrapoxy.io/integration/python/scrapy/guide).


### Step 7: Execute the spider

Run your spider and check that Scrapoxy is handling the requests:

![Scrapoxy Proxies](images/scrapoxy-proxies.png)

You should observe an increase in the count of received and sent requests.

<details>
    <summary>Soluce is here</summary>
    <a href="solutions/challenge-3.py">Open the soluce</a>
</details>


## Challenge 4: IP Detection

The URL to scrape is: [https://trekky-reviews.com/level4](https://trekky-reviews.com/level4)

Update the URL in your scraper to target the new page and execute the spider:

```shell
scrapy crawl trekky
```

Data collection might fail due to the use of **datacenter proxies**.

Datacenter proxies from cloud providers are **frequently detected** by commercial anti-bot systems.
To bypass this, we need more sophisticated proxies.

Scrapoxy offers support for many connectors to different proxy services. 
Today, we will integrate one of these services, which has provided free credits for the workshop.

Refer to [Scrapoxy's documentation](https://scrapoxy.io/intro/scrapoxy) to add this provider.

<table>
    <tr>
        <td width="70">
            <img src="images/warning.png" />
        </td>
        <td>
            Don't forget to stop the cloud provider connector
        </td>
    </tr>
</table>

<details>
    <summary>Soluce is here</summary>
    <a href="solutions/challenge-4.py">Open the soluce</a>
</details>


## Challenge 5: Fingerprint

The URL to scrape is: [https://trekky-reviews.com/level6](https://trekky-reviews.com/level6) (we will skip level5).

Update the URL in your scraper to target the new page and execute the spider:

```shell
scrapy crawl trekky
```

Data collection may fail due to **fingerprinting**.

Use the Network Inspector in your browser to view all requests. 
You will notice a new request appearing, which is a POST request instead of a GET request.

![Chrome Network Inspector List](images/chrome-network-inspector-list.png)

Inspect the website's code to identify the JavaScript that triggers this request.

![Chrome Network Inspector](images/chrome-network-inspector-initiator.png)

It's clear that we need to **execute JavaScript**. 
Simply using Scrapy to send HTTP requests is not enought.

We will use the headless framework [Playwright](https://playwright.dev) along with Scrapy's plugin [scrapy-playwright](https://github.com/scrapy-plugins/scrapy-playwright).

<table>
    <tr>
        <td width="70">
            <img src="images/info.png" />
        </td>
        <td>
            <a href="https://github.com/scrapy-plugins/scrapy-playwright">scrapy-playwright</a> should already be installed.
        </td>
    </tr>
</table>

Our goal is to adapt the spider to integrate Playwright:

* Update the settings to include a custom `DOWNLOAD_HANDLERS`.
* Configure Playwright sessions `PLAYWRIGHT_LAUNCH_OPTIONS` to:
  * Disable headless mode (allowing you to see Playwright's actions)
  * Use a proxy (redirecting traffic through Scrapoxy)
* Attach metadata to each request to enable Playwright and ignore HTTPS errors (using ignore_https_errors).

<details>
    <summary>Soluce is here</summary>
    <a href="solutions/challenge-5.py">Open the soluce</a>
</details>


## Challenge 6: Consistency

The URL to scrape is: [https://trekky-reviews.com/level7](https://trekky-reviews.com/level7)

Update the URL in your scraper to target the new page and execute the spider:

```shell
scrapy crawl trekky
```

You will notice that data collection may fail due to **inconsistency** errors.

Anti-bot checks consistency across various layers of the browser stack.

Try to solve these errors!

Hint: It involves adjusting timezones 😉

<details>
    <summary>Soluce is here</summary>
    <a href="solutions/challenge-6.py">Open the soluce</a>
</details>


## Challenge 7: Deobfuscation

The URL to scrape is: [https://trekky-reviews.com/level8](https://trekky-reviews.com/level8)

Update the URL in your scraper to target the new page and execute the spider:

```shell
scrapy crawl trekky
```

### Step 1: Find the Anti-Bot Javascript

Use the **Network Inspector** to review all requests.
Among them, you'll spot some unusual ones. 
By inspecting the payload, you'll notice that the content is **encrypted**:

![Chrome Network Inspector - List 2](images/chrome-network-inspector-list2.png)

Inspect the website's code to find the JavaScript responsible for sending this requests.
In this case, the source code is obfuscated.
To understand which information is being sent and how to emulate it, we need to **deobfuscate the code**.


### Step 2: Deobfuscate the Javascript

Copy/paste the code of this obfuscated script to `tools/obfuscated.js`.

And run the deobfucator script:

```shell
node tools/deobfuscate.js
```

This script currently doesn't perform any operations.
Our goal is to add [AST](https://en.wikipedia.org/wiki/Abstract_syntax_tree) operations to transform and deobfuscate the code.

<table>
    <tr>
        <td width="70">
            <image src="images/note.png">
        </td>
        <td>
            Of course, you can use <a href="https://obf-io.deobfuscate.io">online tools</a> to deobfuscate this script,
given that it's a straightforward obfuscated script. 
            However, our focus is to understand how Babel can be used for deobfuscation.
        </td>
    </tr>
</table>

<table>
    <tr>
        <td width="70">
            <image src="images/info.png">
        </td>
        <td>
            <a href="https://github.com/features/copilot">GitHub Copilot</a>
            can provide a huge assistance in writing AST operations.
        </td>
    </tr>
</table>

To understand the structure of the code, copy/paste some code into the website [AST Explorer](https://astexplorer.net)

Don't forget to select `@babel/parser` and enable `Transform`:

![AST Explorer Header](images/ast-header.png)

AST Explorer parses the source code and generates a visual tree:

![AST Explorer UI](images/ast-ui.png)

<table>
    <tr>
        <td width="70">
            <image src="images/info.png">
        </td>
        <td>
            I only obfuscated strings, not the code flow.
        </td>
    </tr>
</table>

Now, you can implement the 3 AST operations:

* **Constant Unfolding**: replace all constants with their respective string values;
* **String Join**: combine strings that have been split into multiple parts;
* **Dot Notation**: convert string notation into dot notation.

<details>
    <summary>Soluce is here</summary>
    <a href="solutions/challenge-7.js">Open the soluce</a>
</details>


## Challenge 8: Payload generation

Here’s a summary of the script’s behavior:

1. It collects WebGL information;
2. It encrypts the data using RSA encryption with an obfuscated public key;
3. It sends the payload to the webserver via a POST request.

We need to do the same in our spider.

Since we will be crafting the payload ourselves, there is **no need** to use Playwright anymore. 
We will simply send the payload **before** initiating any requests.

You can use the Python's `Crypto` and `base64` libraries.

<table>
    <tr>
        <td width="70">
            <image src="images/note.png">
        </td>
        <td>
            <ul>
                <li>
                    Crypto.RSA.importKey requires a PEM key format such as:<br/>
                    <code>
                        -----BEGIN PUBLIC KEY-----<br/>
                        MY_PUBLIC_KEY<br/>
                        -----END PUBLIC KEY-----
                    </code>
                </li>
                <li>RSA uses OAEP</li>
                <li>Don't forget the SHA256 signature</li>
            </ul>
        </td>
    </tr>
</table>

<details>
    <summary>Soluce is here</summary>
    <a href="solutions/challenge-8.py">Open the soluce</a>
</details>


## Conclusion

Thank you so much for participating in this workshop.

Your feedback is incredibly valuable to me. 
Please take a moment to complete this survey; your insights will greatly assist in enhancing future workshops:

👉 [GO TO SURVEY](https://bit.ly/scwsv) 👈


## Licence

WebScraping Anti-Ban Workshop © 2024 by [Fabien Vauchelles](https://www.linkedin.com/in/fabienvauchelles) is licensed under [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/?ref=chooser-v1):

* Credit must be given to the creator;
* Only noncommercial use of your work is permitted;
* No derivatives or adaptations of your work are permitted.

