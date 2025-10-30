import { useEffect, useState, type ChangeEvent, type FormEvent } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

type messageObject = {
	message: string[]
}

function App() {

	const [selectedFile, setSelectedFile] = useState<File | null>(null);
	const [mySplitFiles, setMySplitFiles] = useState<string[] | null>(null);

	const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
		const file = event.target.files?.[0] || null;
		setSelectedFile(file);
	};

	const [padding, setPadding] = useState<number>(0);

	const handlePaddingChange = (event: ChangeEvent<HTMLInputElement>) => {
		const value = parseInt(event.target.value, 10); // remember this is binary interpreted so 10 in binary is actually 2 in decimal
		setPadding(isNaN(value) ? 0 : value);
	};


	const handleSendFileForm = async (e: FormEvent) => {
		e.preventDefault();
		if (!selectedFile) return;

		const formData = new FormData();
		formData.append("padding", String(padding))
		formData.append("file", selectedFile);

		const res = await fetch("http://127.0.0.1:8000/split-vid", {
			method: "POST",
			body: formData,
		});


		const data: messageObject = await res.json();
		console.log(data.message);

		setMySplitFiles(data.message)

	};

	const downloadVideo = async (file_name: string) => {
		const url = "http://127.0.0.1:8000/get-vid/" + file_name
		const res = await fetch(url, {
			method: "get"
		});

		const blob = await res.blob();
		const blob_url = URL.createObjectURL(blob)

		const link = Object.assign(document.createElement("a"), {
			href: blob_url,
			download: file_name,
		});
		link.click()
	}



	return (
		<>
			<div>
			</div>
			<h1>KeepItRolling</h1>
			<form onSubmit={handleSendFileForm}>
				<input type="number" placeholder="padding" onChange={handlePaddingChange} />
				<br />
				<input type="file" onChange={handleFileChange} />
				<br />
				<br />
				<button type='submit'>Split</button>
			</form>

			{mySplitFiles?.map((val, idx) => (
				<button onClick={() => { downloadVideo(val) }} value={val} key={idx}></button>
			))}

		</>
	)
}

export default App
