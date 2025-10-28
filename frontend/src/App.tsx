import { useState, type ChangeEvent, type FormEvent } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

type messageObject = {
	message: string[]
}

function App() {

	const [selectedFile, setSelectedFile] = useState<File | null>(null);

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

		data.message.forEach((output: string) => {
			console.log(output)
		}

		);
	};


	return (
		<>
			<div>
				<a href="https://vite.dev" target="_blank">
					<img src={viteLogo} className="logo" alt="Vite logo" />
				</a>
				<a href="https://react.dev" target="_blank">
					<img src={reactLogo} className="logo react" alt="React logo" />
				</a>
			</div>
			<h1>KeepItRolling</h1>
			<form onSubmit={handleSendFileForm}>
				<input type="number" onChange={handlePaddingChange} />
				<input type="file" onChange={handleFileChange} />
				<button type='submit' />
			</form>

		</>
	)
}

export default App
