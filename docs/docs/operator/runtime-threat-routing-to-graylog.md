# How to Route Kubescape Threat Detection Alerts to Graylog Using HTTP Raw Input

This guide shows how to configure the Kubescape operator to send alerts directly to a Graylog HTTP Raw/Plaintext input.

---

## 1. **Create a Raw/Plaintext HTTP Input in Graylog**

1. In the Graylog web UI, go to **System > Inputs**.
2. Select **Raw/Plaintext HTTP** from the dropdown and click **Launch new input**.
3. Choose the node, set the port (e.g., `5555`), and click **Save**.
4. Note the endpoint:
   - **URL:** `http://graylog.graylog.svc.cluster.local:5555/raw`
   (Replace `graylog` and port if you used different values.)

---

## 2. **Configure Kubescape Node-Agent to Use HTTP Raw**

Edit the `node-agent` ConfigMap in the `kubescape` namespace:

```bash
kubectl edit cm -n kubescape node-agent
```

Update the `exporters` section in `config.json` to:

```json
"exporters": {
  "alertManagerExporterUrls": [],
  "stdoutExporter": true,
  "syslogExporterURL": "",
  "httpExporterConfig": {
    "url": "http://graylog.graylog.svc.cluster.local:5555",
    "method": "POST",
    "path": "/raw"
  }
}
```

- Make sure the `url` and `path` match your Graylog input.
- Save and exit.

---

## 3. **Restart the Node-Agent**

Apply the new configuration by restarting the node-agent pods:

```bash
kubectl rollout restart deployment -n kubescape node-agent
```

---

## 4. **Verify Alerts in Graylog**

- Trigger a Kubescape alert (e.g., by `cat /etc/shadow` in one of the pods).
- In Graylog, go to **Search** or your stream to see incoming messages.

---

## 5. **Troubleshooting**

- **No messages in Graylog?**
  - Check the node-agent pod logs for errors.
  - Ensure the Graylog input is running and listening on the correct port.
  - Confirm network connectivity between Kubescape and Graylog.

- **Messages not parsed as expected?**
  - The Raw/Plaintext input treats each POST body as a single message.
    You may want to adjust Kubescape’s output format or use Graylog extractors to parse the JSON.

---

## **Summary**

- Use Graylog’s Raw/Plaintext HTTP input for simple, reliable alert ingestion.
- Point Kubescape’s `httpExporterConfig` to the input’s URL and path.
- Restart node-agent pods to apply changes.
