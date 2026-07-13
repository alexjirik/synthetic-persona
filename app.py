<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Roundpeg | Synthetic Mindset Engine</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        body { font-family: 'Inter', sans-serif; background-color: #f3f4f6; }
        .glass-panel { background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.2); }
        .rp-orange { color: #F26A21; }
        .bg-rp-orange { background-color: #F26A21; }
        .border-rp-orange { border-color: #F26A21; }
        /* Custom scrollbar */
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: #94a3b8; }
    </style>
</head>
<body class="h-screen flex overflow-hidden text-slate-800">

    <!-- Sidebar -->
    <aside class="w-64 bg-slate-900 text-white flex flex-col justify-between hidden md:flex shrink-0">
        <div>
            <div class="h-16 flex items-center px-6 border-b border-slate-800">
                <i class="fa-solid fa-layer-group text-2xl mr-3 rp-orange"></i>
                <span class="text-lg font-bold tracking-wider">ROUNDPEG</span>
            </div>
            <nav class="p-4 space-y-2">
                <a href="#" class="flex items-center space-x-3 bg-slate-800 text-white px-4 py-3 rounded-lg font-medium transition-colors">
                    <i class="fa-solid fa-brain w-5"></i>
                    <span>Synthesis Engine</span>
                </a>
                <a href="#" class="flex items-center space-x-3 text-slate-400 hover:text-white hover:bg-slate-800 px-4 py-3 rounded-lg font-medium transition-colors">
                    <i class="fa-solid fa-chart-pie w-5"></i>
                    <span>Simmons Crosstabs</span>
                </a>
                <a href="#" class="flex items-center space-x-3 text-slate-400 hover:text-white hover:bg-slate-800 px-4 py-3 rounded-lg font-medium transition-colors">
                    <i class="fa-solid fa-book-open w-5"></i>
                    <span>Qual Repository</span>
                </a>
                <a href="#" class="flex items-center space-x-3 text-slate-400 hover:text-white hover:bg-slate-800 px-4 py-3 rounded-lg font-medium transition-colors">
                    <i class="fa-solid fa-cloud-arrow-up w-5"></i>
                    <span>Data Ingestion</span>
                </a>
            </nav>
        </div>
        <div class="p-4 border-t border-slate-800">
            <div class="flex items-center space-x-3">
                <div class="w-8 h-8 rounded-full bg-rp-orange flex items-center justify-center text-sm font-bold">
                    S
                </div>
                <div class="text-sm">
                    <p class="font-medium">Strategist</p>
                    <p class="text-slate-400 text-xs">Sandbox Mode</p>
                </div>
            </div>
        </div>
    </aside>

    <!-- Main Content -->
    <main class="flex-1 flex flex-col h-screen overflow-hidden relative">
        
        <!-- Header -->
        <header class="h-16 glass-panel flex items-center justify-between px-8 shrink-0 z-10">
            <div>
                <h1 class="text-xl font-bold text-slate-800">Synthetic Mindset Engine</h1>
                <p class="text-xs text-slate-500 font-medium tracking-wide uppercase">Fusing Quant Predispositions with Qual Truths</p>
            </div>
            <div class="flex space-x-4">
                <button class="px-4 py-2 bg-white border border-slate-200 text-slate-600 rounded-md text-sm font-medium hover:bg-slate-50 transition shadow-sm flex items-center">
                    <i class="fa-solid fa-download mr-2"></i> Export Report
                </button>
                <button class="px-4 py-2 bg-rp-orange text-white rounded-md text-sm font-medium hover:bg-orange-600 transition shadow-sm flex items-center">
                    <i class="fa-solid fa-wand-magic-sparkles mr-2"></i> Auto-Synthesize
                </button>
            </div>
        </header>

        <!-- Content Area -->
        <div class="flex-1 overflow-y-auto p-8">
            
            <!-- Segment Selector -->
            <div class="mb-8">
                <h2 class="text-sm font-bold text-slate-400 uppercase tracking-wider mb-3">Select Mindset Target</h2>
                <div class="flex flex-wrap gap-2" id="segment-selector">
                    <!-- Buttons injected via JS -->
                </div>
            </div>

            <div class="grid grid-cols-1 xl:grid-cols-3 gap-8">
                
                <!-- Left Column: The Simmons Quant Layer -->
                <div class="xl:col-span-1 space-y-6">
                    
                    <!-- KPI Cards -->
                    <div class="grid grid-cols-2 gap-4">
                        <div class="bg-white p-5 rounded-xl shadow-sm border border-slate-100">
                            <p class="text-xs font-semibold text-slate-500 uppercase tracking-wide mb-1">Pop Size</p>
                            <p class="text-2xl font-bold text-slate-800" id="ui-pop-size">--</p>
                            <p class="text-xs text-emerald-500 font-medium mt-1"><i class="fa-solid fa-arrow-trend-up mr-1"></i> Highly Viable</p>
                        </div>
                        <div class="bg-white p-5 rounded-xl shadow-sm border border-slate-100">
                            <p class="text-xs font-semibold text-slate-500 uppercase tracking-wide mb-1">Median HHI</p>
                            <p class="text-2xl font-bold text-slate-800" id="ui-hhi">--</p>
                            <p class="text-xs text-slate-400 font-medium mt-1">Above Average</p>
                        </div>
                    </div>

                    <!-- Chart -->
                    <div class="bg-white p-6 rounded-xl shadow-sm border border-slate-100">
                        <h3 class="text-sm font-bold text-slate-800 mb-4 flex items-center">
                            <i class="fa-solid fa-chart-bar mr-2 text-slate-400"></i> Top Indexing Traits
                        </h3>
                        <div class="relative h-64 w-full">
                            <canvas id="indexChart"></canvas>
                        </div>
                        <p class="text-[10px] text-slate-400 text-center mt-3">*Simmons Index: >120 is significant</p>
                    </div>

                    <!-- Demos -->
                    <div class="bg-white p-6 rounded-xl shadow-sm border border-slate-100">
                        <h3 class="text-sm font-bold text-slate-800 mb-4 flex items-center">
                            <i class="fa-solid fa-users mr-2 text-slate-400"></i> Defining Demographics
                        </h3>
                        <ul class="space-y-3 text-sm text-slate-600" id="ui-demos">
                            <!-- Injected via JS -->
                        </ul>
                    </div>

                </div>

                <!-- Right Column: The Qualitative Layer -->
                <div class="xl:col-span-2 space-y-6">
                    
                    <!-- Header -->
                    <div class="bg-white p-8 rounded-xl shadow-sm border border-slate-100 relative overflow-hidden">
                        <div class="absolute top-0 left-0 w-1.5 h-full bg-rp-orange"></div>
                        <h2 class="text-3xl font-extrabold text-slate-800 mb-2" id="ui-title">Select a Mindset</h2>
                        <p class="text-lg text-slate-500 italic" id="ui-tagline">...</p>
                    </div>

                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                        
                        <!-- Anthropology -->
                        <div class="bg-white p-6 rounded-xl shadow-sm border border-slate-100">
                            <h3 class="text-sm font-bold text-slate-800 mb-4 flex items-center uppercase tracking-wide">
                                <i class="fa-solid fa-globe mr-2 rp-orange"></i> Online Anthropology
                            </h3>
                            <p class="text-sm text-slate-600 leading-relaxed mb-4" id="ui-anthro">...</p>
                            <div class="bg-slate-50 p-4 rounded-lg border border-slate-100">
                                <p class="text-xs font-bold text-slate-500 uppercase mb-2">Media Diet</p>
                                <p class="text-sm font-medium text-slate-700" id="ui-media">...</p>
                            </div>
                        </div>

                        <!-- Brand & Motivations -->
                        <div class="bg-white p-6 rounded-xl shadow-sm border border-slate-100">
                            <h3 class="text-sm font-bold text-slate-800 mb-4 flex items-center uppercase tracking-wide">
                                <i class="fa-solid fa-heart mr-2 rp-orange"></i> Values & Motivations
                            </h3>
                            <div class="space-y-4">
                                <div>
                                    <p class="text-xs font-bold text-slate-500 uppercase mb-1">What they value</p>
                                    <p class="text-sm text-slate-600" id="ui-value">...</p>
                                </div>
                                <div>
                                    <p class="text-xs font-bold text-slate-500 uppercase mb-1">Top Motivations</p>
                                    <p class="text-sm text-slate-600" id="ui-motivations">...</p>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- The Human Truth -->
                    <div class="bg-slate-800 p-8 rounded-xl shadow-lg border border-slate-700 text-white relative overflow-hidden">
                        <div class="absolute -right-10 -top-10 opacity-10">
                            <i class="fa-solid fa-quote-right text-9xl"></i>
                        </div>
                        <h3 class="text-xs font-bold text-rp-orange mb-4 flex items-center uppercase tracking-widest">
                            <i class="fa-solid fa-bolt mr-2"></i> The Human Truth
                        </h3>
                        
                        <div class="mb-5">
                            <p class="text-xs text-slate-400 uppercase font-bold mb-1 tracking-wide">The Tension</p>
                            <p class="text-base font-medium leading-relaxed" id="ui-tension">...</p>
                        </div>
                        
                        <div class="pt-5 border-t border-slate-700">
                            <p class="text-xs text-slate-400 uppercase font-bold mb-1 tracking-wide">The Ultimate Truth</p>
                            <p class="text-lg font-bold leading-relaxed text-rp-orange" id="ui-truth">...</p>
                        </div>
                    </div>

                </div>
            </div>
        </div>
    </main>

    <script>
        // The Roundpeg Mindset Database (Hardcoded for prototype)
        const mindsetData = {
            "Moment Makers": {
                tagline: "Capable, competent and charismatic. Driven, confident, and fueled by purpose and pride.",
                popSize: "15.0M",
                hhi: "$104K",
                anthro: "Leisure means sports and getting outdoors (Freshwater fishing, weight lifting). They are highly engaged with live, high-adrenaline sports like UFC and NFL.",
                media: "Informative, practical, and action-oriented. Heavy consumers of Consumer Reports and sports broadcasting.",
                value: "Power, Performance, Passion. They want to know what goes on 'under the hood'.",
                motivations: "Excitement, connection, and letting loose. They consider themselves enthusiasts and born leaders.",
                tension: "They crave raw, unfiltered experiences but feel increasingly boxed in by a digitized, hands-off world that lacks tangible thrills.",
                truth: "They need brands that deliver tangible power and performance, enabling them to assert their presence, mastery, and let loose.",
                demos: [
                    "Generation X & Older Millennials (Index: 125)",
                    "Married with children (Index: 115)",
                    "Employed Full Time (Index: 134)"
                ],
                chartLabels: ["I am a born leader", "Good at fixing things", "Under the hood interest", "Life should be fun", "Sacrifice for family"],
                chartData: [135, 184, 150, 142, 120]
            },
            "Expressive Escapists": {
                tagline: "Determined, discerning, and developing. They use standout choices as a personal canvas.",
                popSize: "4.5M",
                hhi: "$88K",
                anthro: "Social media is their stage. They are disproportionately engaged with pop culture, hip-hop concerts, and use digital media to maintain a high-visibility social status.",
                media: "Connection and entertainment. Highly influenced by celebrities, influencers, and trending visual platforms.",
                value: "Fun, Freedom, and Fashionable aesthetics. Exterior styling is their absolute first consideration.",
                motivations: "They want to be seen, celebrated, and set apart. They seek spirited performance that matches their energy.",
                tension: "They want to assert their unique identity but struggle to find platforms and products that feel truly authentic rather than mass-produced.",
                truth: "They gravitate toward brands that act as amplifiers for their personality, offering bold, innovative designs that stand apart.",
                demos: [
                    "Gen Z & Younger Millennials (Index: 143)",
                    "Single / Unmarried (Index: 128)",
                    "Urban / Metro Centers (Index: 135)"
                ],
                chartLabels: ["Car expresses personality", "Stand out in a crowd", "Thrills & Recognition", "Exterior styling is #1", "Spontaneous behavior"],
                chartData: [166, 176, 148, 187, 133]
            },
            "Blue Mindset": {
                tagline: "Grounded, practical, and content. They find fulfillment in routine and close connections.",
                popSize: "42.9M",
                hhi: "$99K",
                anthro: "They consume media carefully, favoring substance over flash. They are skeptical of advertising and prefer thoughtful content that informs rather than distracts.",
                media: "PBS, Consumer Reports, The Atlantic, and documentaries. Quiet, reliable information sources.",
                value: "Dependability, practicality, and a well-ordered life. They avoid unnecessary risks and flashy upgrades.",
                motivations: "Quiet enjoyment, protecting their family, and maintaining a comfortable standard of living.",
                tension: "They are overwhelmed by the constant noise, flash, and anxiety of modern social expectations and digital culture.",
                truth: "They require brands that are dependable, liberating, and simplify their lives without demanding excessive attention.",
                demos: [
                    "Baby Boomers & Gen X (Index: 130)",
                    "Homeowners (Index: 118)",
                    "Suburban/Rural (Index: 122)"
                ],
                chartLabels: ["Vehicle is just transport", "Perfectly happy w/ standard", "Family works well", "Skeptical of ads", "Set routines"],
                chartData: [137, 130, 155, 144, 128]
            }
        };

        let currentChart = null;

        function loadMindset(name) {
            const data = mindsetData[name];
            
            // Update UI text
            document.getElementById('ui-title').innerText = name;
            document.getElementById('ui-tagline').innerText = `"${data.tagline}"`;
            document.getElementById('ui-pop-size').innerText = data.popSize;
            document.getElementById('ui-hhi').innerText = data.hhi;
            document.getElementById('ui-anthro').innerText = data.anthro;
            document.getElementById('ui-media').innerText = data.media;
            document.getElementById('ui-value').innerText = data.value;
            document.getElementById('ui-motivations').innerText = data.motivations;
            document.getElementById('ui-tension').innerText = data.tension;
            document.getElementById('ui-truth').innerText = data.truth;

            // Update Demos
            const demoList = document.getElementById('ui-demos');
            demoList.innerHTML = '';
            data.demos.forEach(d => {
                demoList.innerHTML += `<li><i class="fa-solid fa-check text-emerald-500 mr-2"></i> ${d}</li>`;
            });

            // Update Active Button Style
            document.querySelectorAll('.mindset-btn').forEach(btn => {
                if(btn.innerText === name) {
                    btn.classList.add('bg-slate-800', 'text-white', 'border-slate-800');
                    btn.classList.remove('bg-white', 'text-slate-600', 'border-slate-200');
                } else {
                    btn.classList.remove('bg-slate-800', 'text-white', 'border-slate-800');
                    btn.classList.add('bg-white', 'text-slate-600', 'border-slate-200');
                }
            });

            // Render Chart
            const ctx = document.getElementById('indexChart').getContext('2d');
            if (currentChart) { currentChart.destroy(); }

            currentChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: data.chartLabels,
                    datasets: [{
                        label: 'Simmons Index Score',
                        data: data.chartData,
                        backgroundColor: '#F26A21',
                        borderRadius: 4
                    }]
                },
                options: {
                    indexAxis: 'y',
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false }
                    },
                    scales: {
                        x: {
                            beginAtZero: true,
                            max: 200,
                            grid: { color: '#f1f5f9' },
                            ticks: { font: { size: 10 } }
                        },
                        y: {
                            grid: { display: false },
                            ticks: { font: { size: 11, family: 'Inter' } }
                        }
                    }
                }
            });
        }

        // Initialize Buttons
        const selectorContainer = document.getElementById('segment-selector');
        Object.keys(mindsetData).forEach(key => {
            const btn = document.createElement('button');
            btn.innerText = key;
            btn.className = 'mindset-btn px-4 py-2 rounded-full text-sm font-medium border transition shadow-sm';
            btn.onclick = () => loadMindset(key);
            selectorContainer.appendChild(btn);
        });

        // Load default
        loadMindset('Moment Makers');

    </script>
</body>
</html>
```

### Why this is the "End Product" Vision:

1.  **No Python Environment Needed:** Because it is built entirely with web standards (HTML/Tailwind/JS), it runs natively in the browser. It doesn't require a server running pandas or a terminal to execute. 
2.  **Immersive UI:** Streamlit stacks elements linearly. In this web build, we use a complex CSS Grid. The Quant data (Left Column) sits seamlessly alongside the Qual data (Right Column).
3.  **Interactive Visualizations:** Instead of a static pandas dataframe, I implemented `Chart.js` to render a beautiful, animated bar chart of the Simmons Index scores.
4.  **Brand Alignment:** It incorporates the "Roundpeg" brand styling, custom fonts, icons, and a layout designed specifically for strategic storytelling rather than just data dumping.

If you click the **"Preview"** button in this collaborative environment, you can actually click through the segments (Moment Makers, Expressive Escapists, Blue Mindset) and watch the charts and ethnographic text animate and update in real-time.
