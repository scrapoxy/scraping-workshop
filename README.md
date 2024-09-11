# Fabien's WebScraping Anti-Ban Workshop

![Header](header.jpg)

## Clone the repository

First, clone this repository:

```shell
git clone https://github.com/fabienvauchelles/scraping-workshop.git
cd scraping-workshop
```


## Introduction

The goal of this workshop is to understand how antibot protections work and how to bypass them.

I created a dedicated website for this workshop [https://trekky-reviews.com](https://trekky-reviews.com).
This website provides a list of accommodations for every city, including reviews.

We will collect **name, email and reviews** for each accommodation.

During this workshop, we will use the following open-source software:

| Framework                            | Description                                                                  |
|--------------------------------------|------------------------------------------------------------------------------|
| [Scrapy](https://scrapy.org)         | the leading framework for web scraping                                       |
| [Scrapoxy](https://scrapoxy.io)      | the super proxies aggregator                                                 |
| [Playwright](https://playwright.dev) | the latest headless browser framework that integrates seamlessly with Scrapy |
| [Babel.js](https://babeljs.io)       | a transpiler used for deobfuscation purposes                                 |

<table>
    <tr>
        <td>
            <img src="images/warning.png" />
        </td>
        <td>
            Scrapoxy and Playwright are not working well together on Windows.
            If you are using Windows, I recommend using a Linux VM or WSL.
        </td>
    </tr>
</table>



## File structure

The scraper can be found at [scrapers/spiders/trekky.py](scrapers/spiders/trekky.py).

All solutions are located in [solutions](solutions).
If you have any difficulties implementing a solution, feel free to copy and paste it. 
However, I recommend taking some time to search and explore to get the most out of the workshop, rather than rushing through it in 10 minutes.


## Installation

Please make sure you have installed the following software:

- Python (version 3 or higher) with virtualenv
- Node.js (version 20 or higher)
- Scrapoxy (with Docker)
- Playwright

If you haven't installed these prerequisites yet, here's some guidance to help you get started:

### Python

*Linux*

On Linux, I suggest installing Python and its packages using standard package management tools like `python3-pip` for Ubuntu. 

Creating a virtual environment is crucial to avoid mixing with your system's Python installation using this [guide](https://virtualenv.pypa.io/en/latest/user_guide.html).

*Windows/Mac*

For Windows or Mac users, I recommend installing Python and managing environments through [Anaconda](https://www.anaconda.com/download).

Create a virtual environment inside Anaconda for this workshop.


### Python libraries

Open a shell and install libraries from `setup.py`:

```shell
pip install -r requirements.txt
```


### Playwright

After installing the python libraries, run the follow command:

```shell
playwright install
```


### Node.js

Install Node.js from the [official website](https://nodejs.org/en/download/) or through the version management [NVM](https://github.com/nvm-sh/nvm)


### Node.js libraries

Open a shell and install libraries from `package.json`:

```shell
npm install
```


### Scrapoxy

If you already have docker, just run

```shell
docker pull fabienvauchelles/scrapoxy
```

Otherwise, use NPM to install Scrapoxy:

```shell
npm install -g scrapoxy
```


## Challenge 1: Create your first Scraper

The URL to scrape is: [https://trekky-reviews.com/level1](https://trekky-reviews.com/level1)

The goal is to collect **names, emails, and reviews** for each accommodation listed.

Open the file [`scrapers/spiders/trekky-reviews`](scrapers/spiders/trekky.py).

In Scrapy, a spider is a Python class with a unique name. Here, the name is `trekky`.

The spider class includes a method called `start_requests`, which defines the initial URLs to scrape. 
When a URL is fetched, the Scrapy engine triggers a callback function. 
This callback function handles the parsing of the data. 
It's also possible to generate new requests from within the callback function, allowing for chaining of requests and callbacks.

The structure of items is defined in the file [`scrapers/items.py`](scrapers/items.py). 
Each item type is represented by a dataclass containing fields and a loader:

* `HotelItem`: name, email, review
* `HotelItemLoader`: loader for HotelItem
* `ReviewItem`: rating
* `ReviewItemLoader`: loader for ReviewItem

Now, fill the different parts of the spider.

To run the spider, open a terminal at the project's root directory and run the following command:

```shell
scrapy crawl trekky
```

Scrapy collects data from **50 accommodations**:

```text
2024-07-05 23:11:43 [trekky] INFO: 

We got: 50 items

```

Check the file `results.csv` to ensure all items were correctly collected.


## Challenge 2: First antibot protection

The URL to scrape is: [https://trekky-reviews.com/level2](https://trekky-reviews.com/level2)

Update the URL in your scraper to target the new page and execute the spider:

```shell
scrapy crawl trekky
```

The data collection may fail due to **an anti-bot system**.

Pay attention to the **messages** explaining why access is blocked and use this information to correct the scraper.


## Challenge 3: Rate limit

The URL to scrape is: [https://trekky-reviews.com/level3](https://trekky-reviews.com/level3)

Update the URL in your scraper to target the new page and execute the spider:

```shell
scrapy crawl trekky
```

The data collection may fail due to **rate limiting**.

<table>
    <tr>
        <td>
            <img src="images/warning.png" />
        </td>
        <td>
            Please don't adjust the delay between requests or the number of concurrent requests; <b>that is not our goal</b>. 
            Imagine we need to collect millions of items within a few hours, and delaying our scraping session is not an option. 
            Instead, we will use proxies.
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


## Challenge 4: IP Detection

The URL to scrape is: [https://trekky-reviews.com/level4](https://trekky-reviews.com/level4)

Update the URL in your scraper to target the new page and execute the spider:

```shell
scrapy crawl trekky
```

The data collection may fail due to **basic proxies**.

Datacenter proxies from cloud providers are **often detected** easily by commercial anti-bot systems.
To overcome this, we require more advanced proxies.

Scrapoxy supports many connectors for different proxy services.
Today, we will integrate one of these services, which has provided free credits for this workshop.

Refer to [Scrapoxy's documentation](https://scrapoxy.io/intro/scrapoxy) to add this provider.

Proxies will be removed after the workshop unless you ask me :)

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


## Challenge 5: Fingerprint

The URL to scrape is: [https://trekky-reviews.com/level6](https://trekky-reviews.com/level6) (we will skip level5).

Update the URL in your scraper to target the new page and execute the spider:

```shell
scrapy crawl trekky
```

The data collection may fail due to **fingerprinting**.

Use the Network Inspector in your browser to view all requests. 
You will observe a new request appearing that is not a GET request, but rather a POST request:

![Chrome Network Inspector List](images/chrome-network-inspector-list.png)

Inspect the website's code to locate the JavaScript responsible for sending this request:

![Chrome Network Inspector](images/chrome-network-inspector-initiator.png)

Now, it's obvious that we need to execute JavaScript. 
Relying solely on Scrapy to send HTTP requests is not enough.

To achieve this, we'll use the headless framework [Playwright](https://playwright.dev) along with Scrapy's plugin [scrapy-playwright](https://github.com/scrapy-plugins/scrapy-playwright).

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

The goal is to adjust the spider to include Playwright:

* Modify the settings to include a specific `DOWNLOAD_HANDLERS`.
* Configure Playwright sessions `PLAYWRIGHT_LAUNCH_OPTIONS` to:
  * Disable headless mode (you can understand what Playwright is doing)
  * Use proxy (traffic is redirected to Scrapoxy) 
* Add metadata to each request to enable Playwright and disregard HTTPS errors (with `ignore_https_errors`).


## Challenge 6: Consistency

The URL to scrape is: [https://trekky-reviews.com/level7](https://trekky-reviews.com/level7)

Update the URL in your scraper to target the new page and execute the spider:

```shell
scrapy crawl trekky
```

You will notice that the data collection may fail due to **inconsistency** errors.

Anti-bot checks consistency across various layers of the browser stack.

Try to resolve these errors.


## Challenge 7: Deobfuscation

The URL to scrape is: [https://trekky-reviews.com/level8](https://trekky-reviews.com/level8)

Update the URL in your scraper to target the new page and execute the spider:

```shell
scrapy crawl trekky
```

Use the Network Inspector to examine all requests. 
Within the list, you'll find some unusual requests. If you inspect the payload, you'll notice that the content is encrypted:

![Chrome Network Inspector - List 2](images/chrome-network-inspector-list2.png)

Inspect the website's code to find the JavaScript responsible for sending this requests.
In this case, the source code is obfuscated.
To understand which information is being sent and how to emulate it, we need to **deobfuscate the code**.

Copy/paste the code of this obfuscated script to `tools/obfuscated.js`.

Run the deobfucator script:

```shell
node tools/deobfuscate.js
```

This script currently performs no operations. 
Our goal is to add tree operations to transform and deobfuscate the code.

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

Now, you should write 3 steps:

* **Constant Unfolding**: replace all constants with their respective string values;
* **String Join**: combine strings that have been split into multiple parts;
* **Dot Notation**: convert string notation into dot notation.


## Challenge 8: Payload generation

Now that you understand the script's behavior:

1. It collects WebGL information;
2. It encrypts data with RSA encryption using an obfuscated public key;
3. It sends the payload to the webserver through a POST request.

We need to do the same in our spider.

Since we will be crafting the payload ourselves, there is **no need** to use Playwright anymore. 
We will simply send the payload before initiating any requests.

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


## Conclusion

Thank you so much for participating in this workshop.

Your feedback is incredibly valuable to me. 
Please take a moment to complete this survey; your insights will greatly assist in enhancing future workshops:

👉 [GO TO SURVEY](https://bit.ly/scwsv) 👈

If you wish to keep your proxy service account, please reach out to me. I will ask them to not close the account within the next hour.


## Licence

WebScraping Anti-Ban Workshop © 2024 by [Fabien Vauchelles](https://www.linkedin.com/in/fabienvauchelles) is licensed under [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/?ref=chooser-v1):

* Credit must be given to the creator;
* Only noncommercial use of your work is permitted;
* No derivatives or adaptations of your work are permitted.

