
#  StackSync Assessment

A secure API built with **Flask**, **Docker**, and **NsJail**.

---

##  Features

-  Executes untrusted Python code
-  Validates syntax and enforces `main()` presence
-  Returns the output of `main()` as JSON as result and stdout (Example req, res given below)
-  Supports standard libraries, `os`, `pandas`, `numpy`
-  Two modes:
  -  Local: sandboxed with **NsJail**
  -  Cloud Run: standard Docker image without NsJail (Cloud Run restricts `clone()` syscall)
-  Docker repository size ~ 85 MB, Uncompressed image size ~430MB
-  Simple and secure API interface

---

##  Live API URL (Google Cloud Run)

```
https://noel-stacksync-333394763670.us-west2.run.app/execute
```

---

##  API: `POST /execute`

### Request:

```json
{
  "script": "import json\ndef main():\n    return {\"msg\": \"Hello from Cloud\"}\nif __name__ == \"__main__\":\n    print(json.dumps(main()))"
}
```

### Response:

```json
{
  "result": { "msg": "Hello from Cloud" },
  "stdout": "{\"msg\": \"Hello from Cloud\"}"
}
```

---

##  Test Locally (with NsJail)

### Build the local image:

```bash
docker build -f Dockerfile.local -t noel-stacksync .
```

### Run locally:

```bash
docker run --rm -p 8080:8080 noel-stacksync
```

### Test the API:

```bash
curl -X POST http://localhost:8080/execute \
  -H "Content-Type: application/json" \
  -d '{"script":"import json\ndef main():\n    return {\"msg\": \"Test local\"}\nif __name__==\"__main__\": print(json.dumps(main()))"}'
```

---

##  Local Sandbox Details (NsJail)

In local mode:

-  Networking is disabled (`-N`)
-  `/proc` is disabled
-  Memory capped to 256MB
-  CPU limited to 1 core
-  Max file write: 10MB
-  Read-only FS except `/tmp`
-  Only `/tmp` is writable
-  Timeout: 5s

---

##  Project Structure

```txt
├── app.py             # Flask app & input validator
├── executor.py        # Python script executor (uses NsJail locally)
├── Dockerfile         # Cloud Run deployment (no NsJail)
├── Dockerfile.local   # Local sandbox mode (NsJail enabled)
├── requirements.txt   # Flask, numpy, pandas
└── README.md          # This file
```

---

##  Requirements Met

- Docker-based API
- Deployable to Cloud Run
- Input validation with AST
- NsJail sandboxing (local only)
- Prints + parses JSON return from `main()`
- Cloud-safe fallback (no syscalls like `clone()`)

---

##  Tips

- Python script **must define `main()`** and it **must return a JSON**:

```python
def main():
    return {"key": "value"}

if __name__ == "__main__":
    import json
    print(json.dumps(main()))
```

---

## Time Spent

**~2 to 2.5 hours**

---

## 👤 Author

**Noel Paul Moses Jangam**

