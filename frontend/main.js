import { Streamlit } from "streamlit-component-lib"

function onRender(event) {
    const args = event.detail
    const websocketUrl = args.websocketUrl

    const statusElem = document.getElementById("status")
    const tsElem = document.getElementById("timestamp")
    const valElem = document.getElementById("value")

    const ws = new WebSocket(websocketUrl)

    ws.onopen = () => {
        statusElem.textContent = "Connected"
    }

    ws.onmessage = (event) => {
        try {
            const data = JSON.parse(event.data)
            tsElem.textContent = new Date(data.timestamp).toLocaleTimeString()
            valElem.textContent = data.value

            // ✅ Always send a plain JSON object
            Streamlit.setComponentValue({
                timestamp: String(data.timestamp),
                value: data.value
            })
        } catch (e) {
            console.error("Failed to parse WebSocket message:", e)
        }
    }

    ws.onclose = () => {
        statusElem.textContent = "Disconnected"
    }

    ws.onerror = (err) => {
        statusElem.textContent = "Error"
        console.error("WebSocket error:", err)
    }
}

// Register with Streamlit
Streamlit.events.addEventListener("renderEvent", onRender)
Streamlit.setComponentReady()
Streamlit.setFrameHeight()
