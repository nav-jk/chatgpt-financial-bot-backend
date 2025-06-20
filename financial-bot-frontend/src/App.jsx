import { useState, useRef } from 'react';
import './App.css';
import RecordRTC from 'recordrtc';

function App() {
  const [recording, setRecording] = useState(false);
  const [botAudioURL, setBotAudioURL] = useState(null);
  const [loading, setLoading] = useState(false);
  const recorderRef = useRef(null);

  const startRecording = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const recorder = new RecordRTC(stream, {
      type: 'audio',
      mimeType: 'audio/webm',
    });
    recorder.startRecording();
    recorderRef.current = recorder;
    setRecording(true);
  };

  const stopRecording = async () => {
    const recorder = recorderRef.current;
    await recorder.stopRecording(() => {
      const blob = recorder.getBlob();
      sendAudio(blob);
      setRecording(false);
    });
  };

  const sendAudio = async (audioBlob) => {
    setLoading(true);
    const formData = new FormData();
    formData.append('file', audioBlob, 'recording.webm');

    try {
      const response = await fetch('http://localhost:8000/talk', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        setBotAudioURL(url);
      } else {
        console.error('Failed:', await response.text());
      }
    } catch (err) {
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  const clearHistory = async () => {
    await fetch('http://localhost:8000/clear');
    alert('Chat history cleared!');
  };

  return (
    <div className="app">
      <h1>🎙️ Finny – Your Financial Assistant</h1>

      {!recording ? (
        <button onClick={startRecording}>🎤 Start Recording</button>
      ) : (
        <button onClick={stopRecording}>⏹️ Stop & Send</button>
      )}

      {loading && <p>Processing your request...</p>}

      {botAudioURL && (
        <div>
          <h3>🔊 Bot Reply</h3>
          <audio controls src={botAudioURL}></audio>
        </div>
      )}

      <button onClick={clearHistory} style={{ marginTop: '20px' }}>
        🧹 Clear Chat History
      </button>
    </div>
  );
}

export default App;
