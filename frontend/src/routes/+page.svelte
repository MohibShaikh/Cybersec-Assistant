<script>
    import { writable } from "svelte/store";
    import "../app.css";

    let ip = "";
    let scanResults = writable(null);
    let loading = writable(false);
    let error = writable("");

    async function scanIP() {
        if (!ip) {
            error.set("Please enter a valid IP address.");
            return;
        }
        loading.set(true);
        scanResults.set(null);
        error.set("");

        try {
            const response = await fetch(`http://127.0.0.1:8000/scan/ip/${ip}`);
            const data = await response.json();
            scanResults.set(data);
        } catch (err) {
            error.set("Failed to fetch scan results. Check the backend.");
        } finally {
            loading.set(false);
        }
    }
</script>

<div class="min-h-screen bg-gradient-to-r from-gray-900 to-gray-800 text-white flex flex-col items-center px-6 py-10">
    <h1 class="text-5xl font-extrabold mt-10 tracking-tight">Cybersecurity AI Agent</h1>
    <p class="mt-4 text-lg text-gray-300">Check if an IP address is malicious</p>

    <div class="flex flex-col sm:flex-row gap-4 mt-8 w-full max-w-lg">
        <input 
            type="text"
            bind:value={ip}
            placeholder="Enter IP address"
            class="flex-1 p-4 rounded-full bg-gray-700 text-white border-2 border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
        />
        <button 
            on:click={scanIP}
            class="px-8 py-4 bg-gradient-to-r from-blue-500 to-indigo-500 hover:from-blue-600 hover:to-indigo-600 transition duration-300 rounded-full font-semibold shadow-lg"
        >
            Scan
        </button>
    </div>

    {#if loading}
        <div class="mt-8">
            <div class="animate-spin rounded-full h-16 w-16 border-t-4 border-b-4 border-blue-500"></div>
        </div>
    {/if}

    {#if error}
        <p class="mt-4 text-red-500 text-lg">{error}</p>
    {/if}

    {#if $scanResults}
        <div class="mt-12 p-8 bg-gray-800 rounded-xl shadow-2xl w-full max-w-3xl">
            <h2 class="text-2xl font-bold">Scan Results for <span class="text-blue-400">{ip}</span></h2>
            
            <div class="mt-6">
                <p class="text-gray-400">Threat Level:</p>
                <span class="inline-block px-4 py-2 mt-2 text-lg font-bold rounded-full bg-green-500">
                    {$scanResults["AI Analysis"] || "Unknown"}
                </span>
            </div>

            <div class="mt-6">
                <p class="text-gray-400">Full API Results:</p>
                <pre class="mt-2 bg-gray-900 p-4 rounded-lg text-sm overflow-x-auto">{JSON.stringify($scanResults, null, 2)}</pre>
            </div>
        </div>
    {/if}
</div>
