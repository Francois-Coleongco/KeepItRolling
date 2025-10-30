import { useState, type ChangeEvent, type FormEvent } from 'react';

type messageObject = {
	message: string[];
};

function App() {
	const [selectedFile, setSelectedFile] = useState<File | null>(null);
	const [mySplitFiles, setMySplitFiles] = useState<string[] | null>(null);
	const [padding, setPadding] = useState<number>(0);
	const [loading, setLoading] = useState<boolean>(false);

	const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
		setSelectedFile(event.target.files?.[0] || null);
	};

	const handlePaddingChange = (event: ChangeEvent<HTMLInputElement>) => {
		const value = parseInt(event.target.value, 10);
		setPadding(isNaN(value) ? 0 : value);
	};

	const handleSendFileForm = async (e: FormEvent) => {
		e.preventDefault();
		if (!selectedFile) return;

		setLoading(true);

		const formData = new FormData();
		formData.append('padding', String(padding));
		formData.append('file', selectedFile);

		try {
			const res = await fetch('http://127.0.0.1:8000/split-vid', {
				method: 'POST',
				body: formData,
			});

			const data: messageObject = await res.json();
			setMySplitFiles(data.message);
		} finally {
			setLoading(false);
		}
	};

	const downloadVideo = async (file_name: string) => {
		const url = `http://127.0.0.1:8000/get-vid?file_name=${encodeURIComponent(file_name)}`;
		const res = await fetch(url);
		const blob = await res.blob();
		const blob_url = URL.createObjectURL(blob);
		const link = document.createElement('a');
		link.href = blob_url;
		link.download = file_name;
		document.body.appendChild(link);
		link.click();
		document.body.removeChild(link);
		URL.revokeObjectURL(blob_url);
	};

	return (
		<div className="min-h-screen bg-gray-900 text-gray-200 font-sans p-4">
			<h1 className="text-4xl sm:text-5xl font-bold text-indigo-400 mb-4">
				KeepItRolling
			</h1>

			<p className="text-gray-300 text-base sm:text-lg mb-6">
				A browser-based AI-powered tool for automatically splitting and tagging video recordings.
				Designed for creators who want to keep the camera rolling without manually sifting
				through hours of footage, it detects speech segments, checks coherence, and extracts coherent speech from videos.
			</p>

			<div className="flex flex-col sm:flex-row items-start sm:items-center gap-4 mb-6 bg-gray-800 p-3 rounded shadow-md">
				<input
					type="file"
					onChange={handleFileChange}
					className="bg-gray-700 text-gray-200 px-3 py-1 rounded focus:outline-none w-full sm:w-auto"
				/>
				<input
					type="number"
					placeholder="Padding"
					onChange={handlePaddingChange}
					className="bg-gray-700 text-gray-200 px-3 py-1 rounded w-full sm:w-28 focus:outline-none"
				/>
				<button
					onClick={handleSendFileForm}
					className="bg-indigo-600 text-white px-4 py-1 rounded hover:bg-indigo-700 transition w-full sm:w-auto"
				>
					Split
				</button>
			</div>

			{loading && (
				<div className="fixed inset-0 flex items-center justify-center bg-black/50 z-50">
					<div className="w-12 h-12 border-4 border-indigo-600 border-t-transparent rounded-full animate-spin"></div>
				</div>
			)}

			<div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 p-2 bg-gray-800 rounded shadow-md">
				{mySplitFiles?.map((val, idx) => (
					<div
						key={idx}
						className="flex flex-col items-center gap-2 bg-gray-700 p-2 rounded"
					>
						<video
							controls
							className="w-full sm:w-48 rounded border border-gray-600"
							src={`http://127.0.0.1:8000/get-vid?file_name=${encodeURIComponent(val)}`}
						/>
						<div className="flex items-center gap-2 w-full justify-between">
							<button
								onClick={() => downloadVideo(val)}
								className="bg-indigo-600 px-2 py-1 text-xs rounded hover:bg-indigo-700 transition truncate w-full"
							>
								{val}
							</button>
						</div>
					</div>
				))}
			</div>
		</div>
	);
}

export default App;
