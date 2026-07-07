import React, { useState, useEffect, useRef } from 'react';
import * as d3 from 'd3';
import axios from 'axios';
import { TrendingUp, Activity, Clock, Percent } from 'lucide-react';

const API_BASE = "http://localhost:8000";

const App = () => {
  const [params, setParams] = useState({
    S: 100, K: 100, T: 1, r: 0.05, sigma: 0.2
  });
  const [result, setResult] = useState(null);
  const [plotData, setPlotData] = useState([]);
  const chartRef = useRef();

  const updateData = async () => {
    try {
      const res = await axios.post(`${API_BASE}/calculate`, params);
      setResult(res.data);
      
      const plotRes = await axios.get(`${API_BASE}/plot`, { params });
      setPlotData(plotRes.data);
    } catch (e) {
      console.error("API Error:", e);
    }
  };

  useEffect(() => {
    updateData();
  }, [params]);

  useEffect(() => {
    if (plotData.length === 0) return;
    
    d3.select(chartRef.current).selectAll("*").remove();
    
    const margin = {top: 20, right: 30, bottom: 40, left: 50};
    const width = 600 - margin.left - margin.right;
    const height = 300 - margin.top - margin.bottom;

    const svg = d3.select(chartRef.current)
      .append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .append("g")
      .attr("transform", `translate(${margin.left},${margin.top})`);

    const x = d3.scaleLinear().domain(d3.extent(plotData, d => d.S)).range([0, width]);
    const y = d3.scaleLinear().domain(d3.extent(plotData, d => d.call)).range([height, 0]);

    svg.append("g").attr("transform", `translate(0,${height})`).call(d3.axisBottom(x));
    svg.append("g").call(d3.axisLeft(y));

    svg.append("path")
      .datum(plotData)
      .attr("fill", "none")
      .attr("stroke", "#3b82f6")
      .attr("stroke-width", 2)
      .attr("d", d3.line().x(d => x(d.S)).y(d => y(d.call)));
  }, [plotData]);

  const InputField = ({ label, name, icon: Icon }) => (
    <div className="flex flex-col gap-2 mb-4">
      <label className="text-sm font-medium text-gray-700 flex items-center gap-2">
        <Icon size={14} /> {label}
      </label>
      <input 
        type="number" 
        className="p-2 border rounded-md text-black" 
        value={params[name]} 
        onChange={(e) => setParams({...params, [name]: parseFloat(e.target.value)})} 
      />
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-50 p-8 font-sans text-gray-900">
      <div className="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-8">
        <div className="bg-white p-6 rounded-xl shadow-sm border">
          <h2 className="text-xl font-bold mb-6">Model Parameters</h2>
          <InputField label="Spot Price (S)" name="S" icon={TrendingUp} />
          <InputField label="Strike Price (K)" name="K" icon={TrendingUp} />
          <InputField label="Time to Expiry (T)" name="T" icon={Clock} />
          <InputField label="Risk-Free Rate (r)" name="r" icon={Percent} />
          <InputField label="Volatility (σ)" name="sigma" icon={Activity} />
        </div>

        <div className="md:col-span-2 space-y-8">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {result && (
              <>
                <div className="bg-blue-600 text-white p-4 rounded-lg shadow">
                  <div className="text-xs opacity-80">Call Price</div>
                  <div className="text-2xl font-bold">${result.call.toFixed(2)}</div>
                </div>
                <div className="bg-indigo-600 text-white p-4 rounded-lg shadow">
                  <div className="text-xs opacity-80">Put Price</div>
                  <div className="text-2xl font-bold">${result.put.toFixed(2)}</div>
                </div>
                <div className="bg-white p-4 rounded-lg shadow border">
                  <div className="text-xs text-gray-500">Delta (Δ)</div>
                  <div className="text-2xl font-bold text-gray-800">{result.delta.toFixed(3)}</div>
                </div>
                <div className="bg-white p-4 rounded-lg shadow border">
                  <div className="text-xs text-gray-500">Gamma (Γ)</div>
                  <div className="text-2xl font-bold text-gray-800">{result.gamma.toFixed(4)}</div>
                </div>
              </>
            )}
          </div>

          <div className="bg-white p-6 rounded-xl shadow-sm border">
            <h3 className="text-lg font-semibold mb-4">Call Price vs Spot Price</h3>
            <div ref={chartRef} className="flex justify-center" />
          </div>
        </div>
      </div>
    </div>
  );
};

export default App;
