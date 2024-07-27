
# Asset Enumeration And Reconnaissance

This tool aims to determine all attack surfaces of the given target in URL format


## Authors

- [@msoneri](https://github.com/msoneri)
- [@YasinCelik01](https://github.com/YasinCelik01)
- [@doganalkim](https://github.com/doganalkim)


## Run on Docker

1 - Clone the repository.

2 - Build the Docker image.
```bash
    sudo docker build -t kali .
```

3 - Run the container.
```bash
    sudo docker run -i -t --name assetenumeration -p 5000:5000 -v $(pwd):/root:rw kali
```

4 - Install the requirements
```
    pip3 install -r requirements.txt
```

5 - Run flask
```bash
    python3 flask_app.py
```


6 - Open your browser and go to http://127.0.0.1:5000

    
## Run Locally

Get help

```bash
  python3 main -h
```


Run on Terminal

```bash
  python3 main -u $TARGET_URL
```

   

![Logo](https://media.istockphoto.com/id/1383933495/vector/hacker-symbol.jpg?s=612x612&w=0&k=20&c=fFR3n51RetENXUg8st7kGoO-ErvWA__ZDEE7CPn-9KM=)

## API Reference

#### Shodan API

If you want to use Shodan API, you shoould enter your API key in config.py file as string format.

```http
	GET /shodan/host/search

```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `api_key` | `string` | **Optional**. Your Shodan API key |

## Features

- Web Interface
- Terminal Execution
- Command Line Arguement


## Related

Here are some tools requiered for project. If the tools below do not work from each directory, execute the command below.

```
cp $tool /usr/bin/
```


- [Nmap](https://nmap.org/)
- [Subfinder](https://github.com/projectdiscovery/subfinder) 
- [masscan](https://github.com/robertdavidgraham/masscan)


## Optimizations

1. Timestamp is the exact time of  beginning of the scan process.
2. During port scanning, each IP address is scanned once. Therefore, changes during the scan may not affact the result.



## Feedback

If you have any feedback, please reach out to us.



