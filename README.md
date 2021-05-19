# time-fc
Code for the time feature collector, which extracts "duration", "time to departure", "rush hour overlap" and "waiting time" for all the offers connected to a given request.

## Usage

### Local development (debug on)

```bash
$ python3 time-fc.py
 * Serving Flask app "time-fc.py" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on all addresses.
   WARNING: This is a development server. Do not use it in a production deployment.
 * Running on http://172.18.0.3:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 494-689-672
```

### Local development with Docker

#### Build the Docker image:

```bash
docker build -t r2r/time-fc:latest .
```

#### Run the Docker container:
```bash
docker run --rm -it --name time -p 5000:5000 --link offer-cache_cache_1:cache -e FLASK_ENV='development' --net cache-network -v "$PWD":/code r2r/time-fc:latest
```

Please note that "cache-network" is the network where the offer-cache container runs when launched with docker-compose. 


## Example Request

```bash
$ curl --header 'Content-Type: application/json' --request POST --data '{"request_id": "#31:4265-#24:10239"}' http://localhost:5000/compute
```
