import React, { useState, useRef } from 'react';

const RhythmDetectorPro = () => {
  const [text, setText] = useState('');
  const [isMonitoring, setIsMonitoring] = useState(false);
  const [events, setEvents] = useState([]);
  const [keystrokeCount, setKeystrokeCount] = useState(0);
  const [results, setResults] = useState(null);
  const [lang, setLang] = useState('en'); // 'en' or 'zh'
  const [isComposing, setIsComposing] = useState(false);
  const [compositionText, setCompositionText] = useState('');
  const [showTooltip, setShowTooltip] = useState(null);
  
  const startTimeRef = useRef(null);
  const lastCompositionRef = useRef('');

  // 多语言文本
  const t = {
    en: {
      title: 'CRPL Rhythm Detector Pro',
      subtitle: 'Celestelin Rhythm Perception Layer • 24 Fields • Chinese/English Support',
      typeHere: 'Type Here',
      placeholder: 'Click here and start typing... Chinese or English!\nExpress your thoughts naturally.',
      recording: 'Recording',
      ready: 'Ready',
      keystrokes: 'keystrokes',
      analyze: 'Analyze',
      reset: 'Reset',
      results: 'Analysis Results',
      baseline: 'Baseline',
      statistics: 'Statistics', 
      deletion: 'Deletion',
      modification: 'Modification',
      burst: 'Burst',
      hesitation: 'Hesitation',
      fluency: 'Fluency',
      pauses: 'Pauses',
      chineseIME: 'Chinese IME Analysis',
      imeEvents: 'IME Events',
      keystrokeRatio: 'Keystroke Ratio',
      pinyinCaptured: 'Pinyin keystrokes captured!',
      typical: 'typical',
      instructions: 'Click the text area and start typing. When finished, click "Analyze" to see your typing rhythm pattern.',
      footer: 'CelestelinAgent Research © 2025 • Yingying Chen & Anran Lin',
      short: 'short',
      medium: 'medium', 
      long: 'long'
    },
    zh: {
      title: 'CRPL 节奏探测器 Pro',
      subtitle: 'Celestelin 节奏感知层 • 24字段 • 支持中英文',
      typeHere: '在这里打字',
      placeholder: '点击这里开始打字...中文或英文都可以！\n自然地表达你的想法。',
      recording: '记录中',
      ready: '就绪',
      keystrokes: '按键',
      analyze: '分析',
      reset: '重置',
      results: '分析结果',
      baseline: '基线指标',
      statistics: '基础统计',
      deletion: '删除分析',
      modification: '修改分析',
      burst: '爆发检测',
      hesitation: '犹豫映射',
      fluency: '流畅评分',
      pauses: '停顿详情',
      chineseIME: '中文输入法分析',
      imeEvents: '输入法事件',
      keystrokeRatio: '按键比率',
      pinyinCaptured: '拼音按键已捕获！',
      typical: '典型值',
      instructions: '点击输入框开始打字，完成后点击「分析」查看你的打字节奏模式。',
      footer: 'CelestelinAgent 研究 © 2025 • 陈滢滢 & 林安然',
      short: '短',
      medium: '中',
      long: '长'
    }
  };

  // 指标解释 (tooltips)
  const tooltips = {
    en: {
      chars_per_minute: 'Characters typed per minute (effective typing speed)',
      rhythm_type: 'Overall typing rhythm classification based on speed, consistency, and pause patterns',
      fluency_score: 'Composite score (0-1) combining stability, deletion rate, pauses, and hesitations',
      fluency_level: 'Categorical fluency level: very_fluent, fluent, normal, or hesitant',
      keystroke_ratio: 'Total keystrokes ÷ actual characters. Chinese IME typically shows 3.0-4.0',
      consistency: 'Rhythm regularity score (0-1). Higher = more consistent typing rhythm',
      duration: 'Total time from first keystroke to analysis',
      pause_pattern: 'Categorized pause style: continuous, choppy, thoughtful, or contemplative',
      text_rhythm: 'Language-level rhythm based on sentence length and punctuation density',
      total_keystrokes: 'All recorded key events including IME composition keys',
      actual_chars: 'Final character count in the text',
      avg_interval: 'Average time between keystrokes in seconds',
      deletion_count: 'Number of backspace/delete events',
      deletion_ratio: 'Deletion events ÷ total keystrokes',
      burst_count: 'Number of rapid typing segments (>5 keys with <150ms intervals)',
      burst_speed: 'Maximum typing speed during burst segments (chars/sec)',
      hesitation_count: 'Number of pauses longer than 3 seconds',
      short_pauses: 'Pauses between 2-5 seconds (word selection, brief thinking)',
      medium_pauses: 'Pauses between 5-15 seconds (sentence planning)',
      long_pauses: 'Pauses over 15 seconds (deep thinking, distraction)',
      // Rhythm type explanations
      steady_fast: 'Fast and consistent typing - confident, skilled expression',
      burst_fast: 'Fast with bursts - inspiration, emotional arousal',
      steady_slow: 'Slow but consistent - careful, deliberate',
      erratic_fast: 'Fast but inconsistent - rushed, agitated',
      hesitant: 'Slow with thinking pauses - uncertain, exploring',
      labored: 'Slow and struggling - difficulty, fatigue',
      fluid: 'Medium speed, very consistent - flow state, natural',
      measured: 'Medium speed with thinking pauses - analytical',
      uneven: 'Medium speed, inconsistent - distracted, interrupted',
      balanced: 'Default/neutral rhythm pattern'
    },
    zh: {
      chars_per_minute: '每分钟输入的字符数（有效打字速度）',
      rhythm_type: '基于速度、一致性和停顿模式的整体节奏分类',
      fluency_score: '综合分数(0-1)，结合稳定性、删除率、停顿和犹豫',
      fluency_level: '流畅度等级：非常流畅、流畅、正常、犹豫',
      keystroke_ratio: '总按键数÷实际字符数。中文输入法典型值为3.0-4.0',
      consistency: '节奏规律性分数(0-1)。越高=打字节奏越稳定',
      duration: '从第一次按键到分析的总时间',
      pause_pattern: '停顿风格分类：连续、断续、深思、沉思',
      text_rhythm: '基于句子长度和标点密度的语言层面节奏',
      total_keystrokes: '所有记录的按键事件，包括输入法组合键',
      actual_chars: '文本中的最终字符数',
      avg_interval: '按键之间的平均间隔（秒）',
      deletion_count: '退格/删除事件数量',
      deletion_ratio: '删除事件÷总按键数',
      burst_count: '快速打字片段数量（>5键且间隔<150ms）',
      burst_speed: '爆发片段中的最高打字速度（字符/秒）',
      hesitation_count: '超过3秒的停顿次数',
      short_pauses: '2-5秒的停顿（词汇选择、短暂思考）',
      medium_pauses: '5-15秒的停顿（句子规划）',
      long_pauses: '超过15秒的停顿（深度思考、注意力转移）',
      // Rhythm type explanations
      steady_fast: '快速且稳定 - 自信、熟练的表达',
      burst_fast: '快速带爆发 - 灵感涌现、情绪激动',
      steady_slow: '缓慢但稳定 - 谨慎、深思熟虑',
      erratic_fast: '快速但不稳定 - 匆忙、焦躁',
      hesitant: '缓慢带思考停顿 - 不确定、探索中',
      labored: '缓慢且吃力 - 困难、疲劳',
      fluid: '中速且非常稳定 - 心流状态、自然',
      measured: '中速带思考停顿 - 分析性思维',
      uneven: '中速但不稳定 - 分心、被打断',
      balanced: '默认/中性节奏模式'
    }
  };

  const txt = t[lang];
  const tip = tooltips[lang];

  // Tooltip组件
  const Tooltip = ({ id, children }) => (
    <span 
      className="relative cursor-help"
      onMouseEnter={() => setShowTooltip(id)}
      onMouseLeave={() => setShowTooltip(null)}
    >
      {children}
      {showTooltip === id && tip[id] && (
        <span className="absolute z-50 bottom-full left-1/2 -translate-x-1/2 mb-2 px-3 py-2 bg-slate-800 text-white text-xs rounded-lg shadow-xl w-64 text-center border border-purple-500/30">
          {tip[id]}
          <span className="absolute top-full left-1/2 -translate-x-1/2 border-4 border-transparent border-t-slate-800"></span>
        </span>
      )}
    </span>
  );

  // 开始监控
  const handleFocus = () => {
    if (!isMonitoring) {
      setIsMonitoring(true);
      startTimeRef.current = Date.now();
      setEvents([]);
      setKeystrokeCount(0);
      setResults(null);
      setCompositionText('');
      lastCompositionRef.current = '';
    }
  };

  // 处理普通按键
  const handleKeyDown = (e) => {
    if (!isMonitoring) return;
    if (isComposing) return;
    
    const timestamp = Date.now();
    
    if (e.key === 'Backspace') {
      setEvents(prev => [...prev, { type: 'backspace', char: '', timestamp }]);
      setKeystrokeCount(prev => prev + 1);
    } else if (e.key === 'Delete') {
      setEvents(prev => [...prev, { type: 'delete', char: '', timestamp }]);
      setKeystrokeCount(prev => prev + 1);
    } else if (e.key === 'Enter') {
      return;
    } else if (e.key.length === 1) {
      setEvents(prev => [...prev, { type: 'type', char: e.key, timestamp }]);
      setKeystrokeCount(prev => prev + 1);
    }
  };

  // 输入法组合开始
  const handleCompositionStart = (e) => {
    if (!isMonitoring) return;
    setIsComposing(true);
    lastCompositionRef.current = '';
    setCompositionText('');
  };

  // 输入法组合更新
  const handleCompositionUpdate = (e) => {
    if (!isMonitoring) return;
    
    const currentData = e.data || '';
    const previousData = lastCompositionRef.current;
    const timestamp = Date.now();
    
    if (currentData.length > previousData.length) {
      const newChars = currentData.slice(previousData.length);
      for (const char of newChars) {
        setEvents(prev => [...prev, { 
          type: 'composition', 
          char: char, 
          timestamp,
          isIME: true 
        }]);
        setKeystrokeCount(prev => prev + 1);
      }
    } else if (currentData.length < previousData.length) {
      const deletedCount = previousData.length - currentData.length;
      for (let i = 0; i < deletedCount; i++) {
        setEvents(prev => [...prev, { 
          type: 'composition_delete', 
          char: '', 
          timestamp,
          isIME: true 
        }]);
        setKeystrokeCount(prev => prev + 1);
      }
    }
    
    lastCompositionRef.current = currentData;
    setCompositionText(currentData);
  };

  // 输入法组合结束
  const handleCompositionEnd = (e) => {
    if (!isMonitoring) return;
    
    const timestamp = Date.now();
    const finalChar = e.data || '';
    
    setEvents(prev => [...prev, { 
      type: 'composition_confirm', 
      char: finalChar, 
      timestamp,
      isIME: true 
    }]);
    setKeystrokeCount(prev => prev + 1);
    
    setIsComposing(false);
    setCompositionText('');
    lastCompositionRef.current = '';
  };

  // 分析节奏
  const analyzeRhythm = () => {
    if (!text.trim() || events.length < 2) {
      alert(lang === 'en' ? 'Please type at least a few characters first!' : '请先输入一些文字！');
      return;
    }

    const endTime = Date.now();
    const totalTime = (endTime - startTimeRef.current) / 1000;
    
    const typeEvents = events.filter(e => 
      e.type === 'type' || e.type === 'composition' || e.type === 'composition_confirm'
    );
    
    const intervals = [];
    for (let i = 1; i < typeEvents.length; i++) {
      intervals.push((typeEvents[i].timestamp - typeEvents[i-1].timestamp) / 1000);
    }

    const avgInterval = intervals.length > 0 
      ? intervals.reduce((a, b) => a + b, 0) / intervals.length 
      : 0;

    let consistency = 0;
    if (intervals.length > 1 && avgInterval > 0) {
      const variance = intervals.reduce((sum, x) => sum + Math.pow(x - avgInterval, 2), 0) / intervals.length;
      const stdDev = Math.sqrt(variance);
      const cv = stdDev / avgInterval;
      consistency = Math.max(0, Math.min(1, 1 - cv / 2));
    }

    const shortPauses = intervals.filter(i => i >= 2 && i < 5).length;
    const mediumPauses = intervals.filter(i => i >= 5 && i < 15).length;
    const longPauses = intervals.filter(i => i >= 15).length;

    let pausePattern = 'continuous';
    if (longPauses > 0) pausePattern = 'contemplative';
    else if (mediumPauses > 0) pausePattern = 'thoughtful';
    else if (shortPauses > 0) pausePattern = 'choppy';

    const hesitationCount = intervals.filter(i => i >= 3).length;
    const hesitations = intervals
      .map((dur, idx) => ({ location: idx, duration: dur }))
      .filter(h => h.duration >= 3);

    // 💜 修复：只计算真正的删除（backspace/delete），不计算输入法内部的composition_delete
    const deletionCount = events.filter(e => 
      e.type === 'backspace' || e.type === 'delete'
    ).length;
    const deletionRatio = events.length > 0 ? deletionCount / events.length : 0;

    let burstCount = 0;
    let burstSegments = [];
    let currentBurst = 0;
    let burstStart = 0;
    let burstTime = 0;

    for (let i = 0; i < intervals.length; i++) {
      if (intervals[i] < 0.15) {
        if (currentBurst === 0) burstStart = i;
        currentBurst++;
        burstTime += intervals[i];
      } else {
        if (currentBurst >= 5) {
          burstCount++;
          burstSegments.push({
            start: burstStart,
            length: currentBurst,
            avg_speed: burstTime > 0 ? currentBurst / burstTime : 0
          });
        }
        currentBurst = 0;
        burstTime = 0;
      }
    }
    if (currentBurst >= 5) {
      burstCount++;
      burstSegments.push({
        start: burstStart,
        length: currentBurst,
        avg_speed: burstTime > 0 ? currentBurst / burstTime : 0
      });
    }

    const maxBurstSpeed = burstSegments.length > 0 
      ? Math.max(...burstSegments.map(s => s.avg_speed))
      : 0;

    const stabilityScore = Math.min(consistency, 1);
    const deletionScore = Math.max(0, 1 - deletionRatio * 2);
    const pauseScore = Math.max(0, 1 - (shortPauses + mediumPauses * 2 + longPauses * 3) / 10);
    const hesitationScore = Math.max(0, 1 - hesitationCount / 5);

    const fluencyScore = stabilityScore * 0.3 + deletionScore * 0.3 + pauseScore * 0.2 + hesitationScore * 0.2;

    let fluencyLevel = 'normal';
    if (fluencyScore >= 0.8) fluencyLevel = 'very_fluent';
    else if (fluencyScore >= 0.6) fluencyLevel = 'fluent';
    else if (fluencyScore < 0.4) fluencyLevel = 'hesitant';

    const cpm = totalTime > 0 ? (text.length / totalTime) * 60 : 0;
    let rhythmType = 'balanced';

    if (cpm > 120 && consistency > 0.7) {
      rhythmType = pausePattern === 'continuous' ? 'steady_fast' : 'burst_fast';
    } else if (cpm < 60 && consistency > 0.7) {
      rhythmType = 'steady_slow';
    } else if (cpm > 120 && consistency < 0.5) {
      rhythmType = 'erratic_fast';
    } else if (cpm < 60 && consistency < 0.5) {
      rhythmType = pausePattern === 'thoughtful' || pausePattern === 'contemplative' ? 'hesitant' : 'labored';
    } else if (consistency > 0.7) {
      rhythmType = 'fluid';
    } else if (pausePattern === 'thoughtful') {
      rhythmType = 'measured';
    } else if (consistency < 0.7) {
      rhythmType = 'uneven';
    }

    const sentences = text.split(/[.!?。！？]+/).filter(s => s.trim());
    const sentenceCount = sentences.length || 1;
    const avgSentenceLength = text.length / sentenceCount;
    const punctuationRate = (text.match(/[.,!?;:，。！？；：～~]/g) || []).length / text.length;

    let textRhythmCategory = 'balanced';
    if (avgSentenceLength < 20 && punctuationRate < 0.05) textRhythmCategory = 'concise';
    else if (avgSentenceLength < 20 && punctuationRate >= 0.05) textRhythmCategory = 'staccato';
    else if (avgSentenceLength >= 50 && punctuationRate < 0.05) textRhythmCategory = 'flowing';
    else if (avgSentenceLength >= 50 && punctuationRate >= 0.08) textRhythmCategory = 'complex';
    else if (punctuationRate >= 0.08) textRhythmCategory = 'punctuated';

    const keystrokeRatio = text.length > 0 ? events.length / text.length : 0;
    const imeEvents = events.filter(e => e.isIME).length;
    const detectedLanguage = imeEvents > events.length * 0.3 ? 'Chinese (IME)' : 'English (Direct)';

    setResults({
      timestamp: new Date().toISOString(),
      duration_seconds: totalTime.toFixed(2),
      chars_per_minute: cpm.toFixed(1),
      pause_pattern: {
        short_pauses: shortPauses,
        medium_pauses: mediumPauses,
        long_pauses: longPauses,
        pattern: pausePattern
      },
      consistency: consistency.toFixed(3),
      text_rhythm: {
        sentence_count: sentenceCount,
        avg_sentence_length: avgSentenceLength.toFixed(1),
        punctuation_rate: punctuationRate.toFixed(3),
        rhythm_category: textRhythmCategory
      },
      rhythm_type: rhythmType,
      total_keystrokes: events.length,
      actual_chars: text.length,
      keystroke_ratio: keystrokeRatio.toFixed(2),
      avg_interval: avgInterval.toFixed(3),
      deletion_count: deletionCount,
      deletion_ratio: deletionRatio.toFixed(3),
      modification_count: 0,
      burst_count: burstCount,
      burst_segments: burstSegments.length,
      max_burst_speed: maxBurstSpeed.toFixed(1),
      hesitation_count: hesitationCount,
      hesitation_locations: hesitations.map(h => h.location),
      fluency_score: fluencyScore.toFixed(3),
      fluency_level: fluencyLevel,
      detected_language: detectedLanguage,
      ime_events: imeEvents
    });

    setIsMonitoring(false);
  };

  const handleReset = () => {
    setText('');
    setEvents([]);
    setKeystrokeCount(0);
    setResults(null);
    setIsMonitoring(false);
    startTimeRef.current = null;
    setCompositionText('');
    setIsComposing(false);
  };

  const getStatusColor = (level) => {
    switch(level) {
      case 'very_fluent': return 'bg-emerald-500';
      case 'fluent': return 'bg-green-500';
      case 'normal': return 'bg-yellow-500';
      case 'hesitant': return 'bg-red-500';
      default: return 'bg-gray-500';
    }
  };

  const getRhythmColor = (type) => {
    if (type.includes('fast') || type === 'fluid') return 'text-emerald-400';
    if (type.includes('slow') || type === 'measured') return 'text-blue-400';
    if (type === 'hesitant' || type === 'labored') return 'text-orange-400';
    return 'text-purple-400';
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 p-4">
      <div className="max-w-6xl mx-auto">
        {/* Header with Language Toggle */}
        <div className="flex justify-between items-start mb-4">
          <div>
            <h1 className="text-2xl font-bold text-white mb-1">🎹 {txt.title}</h1>
            <p className="text-purple-300 text-sm">{txt.subtitle}</p>
          </div>
          <div className="flex items-center gap-2 bg-slate-800/50 rounded-lg p-1">
            <button
              onClick={() => setLang('en')}
              className={`px-3 py-1 rounded text-sm font-medium transition-colors ${lang === 'en' ? 'bg-purple-600 text-white' : 'text-gray-400 hover:text-white'}`}
            >
              EN
            </button>
            <button
              onClick={() => setLang('zh')}
              className={`px-3 py-1 rounded text-sm font-medium transition-colors ${lang === 'zh' ? 'bg-purple-600 text-white' : 'text-gray-400 hover:text-white'}`}
            >
              中文
            </button>
          </div>
        </div>

        {/* Input Section */}
        <div className="bg-white/10 backdrop-blur rounded-2xl p-4 mb-4 border border-purple-500/30">
          <div className="flex items-center justify-between mb-3">
            <h2 className="text-base font-semibold text-white">📝 {txt.typeHere}</h2>
            <div className="flex items-center gap-3">
              <span className={`px-2 py-1 rounded-full text-xs font-medium ${isMonitoring ? 'bg-green-500 text-white' : 'bg-gray-600 text-gray-300'}`}>
                {isMonitoring ? `🟢 ${txt.recording}` : `⚪ ${txt.ready}`}
              </span>
              <span className="text-purple-300 text-xs">
                ⌨️ {keystrokeCount} {txt.keystrokes}
              </span>
              {isComposing && (
                <span className="text-amber-400 text-xs">
                  🔤 IME: {compositionText}
                </span>
              )}
            </div>
          </div>
          
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            onFocus={handleFocus}
            onKeyDown={handleKeyDown}
            onCompositionStart={handleCompositionStart}
            onCompositionUpdate={handleCompositionUpdate}
            onCompositionEnd={handleCompositionEnd}
            placeholder={txt.placeholder}
            className="w-full h-24 p-3 rounded-xl bg-slate-800 text-white placeholder-gray-400 border border-purple-500/30 focus:border-purple-400 focus:outline-none resize-none"
          />
          
          <div className="flex gap-3 mt-3">
            <button
              onClick={analyzeRhythm}
              className="px-5 py-2 bg-purple-600 hover:bg-purple-500 text-white rounded-lg font-medium transition-colors text-sm"
            >
              📊 {txt.analyze}
            </button>
            <button
              onClick={handleReset}
              className="px-5 py-2 bg-slate-600 hover:bg-slate-500 text-white rounded-lg font-medium transition-colors text-sm"
            >
              🔄 {txt.reset}
            </button>
          </div>
        </div>

        {/* Results Section */}
        {results && (
          <div className="bg-white/10 backdrop-blur rounded-2xl p-4 border border-purple-500/30">
            <div className="flex items-center justify-between mb-3">
              <h2 className="text-base font-semibold text-white">📊 {txt.results}</h2>
              <span className={`px-2 py-1 rounded-full text-xs ${results.detected_language.includes('Chinese') ? 'bg-red-500' : 'bg-blue-500'} text-white`}>
                {results.detected_language}
              </span>
            </div>
            
            {/* Key Metrics */}
            <div className="grid grid-cols-5 gap-2 mb-4">
              <Tooltip id="chars_per_minute">
                <div className="bg-slate-800/50 rounded-xl p-3 text-center cursor-help">
                  <div className="text-2xl font-bold text-cyan-400">{results.chars_per_minute}</div>
                  <div className="text-gray-400 text-xs">chars/min</div>
                </div>
              </Tooltip>
              
              <Tooltip id={results.rhythm_type}>
                <div className="bg-slate-800/50 rounded-xl p-3 text-center cursor-help">
                  <div className={`text-lg font-bold ${getRhythmColor(results.rhythm_type)}`}>
                    {results.rhythm_type}
                  </div>
                  <div className="text-gray-400 text-xs">rhythm</div>
                </div>
              </Tooltip>
              
              <Tooltip id="fluency_score">
                <div className="bg-slate-800/50 rounded-xl p-3 text-center cursor-help">
                  <div className="text-2xl font-bold text-amber-400">{results.fluency_score}</div>
                  <div className="text-gray-400 text-xs">fluency</div>
                </div>
              </Tooltip>
              
              <Tooltip id="keystroke_ratio">
                <div className="bg-slate-800/50 rounded-xl p-3 text-center cursor-help">
                  <div className="text-2xl font-bold text-pink-400">{results.keystroke_ratio}</div>
                  <div className="text-gray-400 text-xs">key ratio</div>
                </div>
              </Tooltip>
              
              <Tooltip id="fluency_level">
                <div className="bg-slate-800/50 rounded-xl p-3 text-center cursor-help">
                  <div className={`text-xs font-bold px-2 py-1 rounded-full inline-block ${getStatusColor(results.fluency_level)} text-white`}>
                    {results.fluency_level}
                  </div>
                  <div className="text-gray-400 text-xs mt-1">level</div>
                </div>
              </Tooltip>
            </div>

            {/* 7 Categories */}
            <div className="grid grid-cols-4 gap-2">
              {/* Baseline */}
              <div className="bg-red-900/20 rounded-xl p-2 border border-red-500/30">
                <h3 className="text-red-400 font-semibold text-xs mb-2">📊 {txt.baseline} (7)</h3>
                <div className="space-y-1 text-xs">
                  <Tooltip id="duration"><div className="flex justify-between cursor-help"><span className="text-gray-400">duration</span><span className="text-white font-mono">{results.duration_seconds}s</span></div></Tooltip>
                  <div className="flex justify-between"><span className="text-gray-400">CPM</span><span className="text-white font-mono">{results.chars_per_minute}</span></div>
                  <Tooltip id="pause_pattern"><div className="flex justify-between cursor-help"><span className="text-gray-400">pause</span><span className="text-white font-mono">{results.pause_pattern.pattern}</span></div></Tooltip>
                  <Tooltip id="consistency"><div className="flex justify-between cursor-help"><span className="text-gray-400">consistency</span><span className="text-white font-mono">{results.consistency}</span></div></Tooltip>
                  <Tooltip id="text_rhythm"><div className="flex justify-between cursor-help"><span className="text-gray-400">text_rhythm</span><span className="text-white font-mono">{results.text_rhythm.rhythm_category}</span></div></Tooltip>
                </div>
              </div>

              {/* Statistics */}
              <div className="bg-orange-900/20 rounded-xl p-2 border border-orange-500/30">
                <h3 className="text-orange-400 font-semibold text-xs mb-2">📈 {txt.statistics} (3)</h3>
                <div className="space-y-1 text-xs">
                  <Tooltip id="total_keystrokes"><div className="flex justify-between cursor-help"><span className="text-gray-400">keystrokes</span><span className="text-white font-mono">{results.total_keystrokes}</span></div></Tooltip>
                  <Tooltip id="actual_chars"><div className="flex justify-between cursor-help"><span className="text-gray-400">chars</span><span className="text-white font-mono">{results.actual_chars}</span></div></Tooltip>
                  <Tooltip id="avg_interval"><div className="flex justify-between cursor-help"><span className="text-gray-400">avg_interval</span><span className="text-white font-mono">{results.avg_interval}s</span></div></Tooltip>
                </div>
              </div>

              {/* Deletion */}
              <div className="bg-yellow-900/20 rounded-xl p-2 border border-yellow-500/30">
                <h3 className="text-yellow-400 font-semibold text-xs mb-2">🔄 {txt.deletion} (3)</h3>
                <div className="space-y-1 text-xs">
                  <Tooltip id="deletion_count"><div className="flex justify-between cursor-help"><span className="text-gray-400">count</span><span className="text-white font-mono">{results.deletion_count}</span></div></Tooltip>
                  <Tooltip id="deletion_ratio"><div className="flex justify-between cursor-help"><span className="text-gray-400">ratio</span><span className="text-white font-mono">{results.deletion_ratio}</span></div></Tooltip>
                </div>
              </div>

              {/* Modification */}
              <div className="bg-green-900/20 rounded-xl p-2 border border-green-500/30">
                <h3 className="text-green-400 font-semibold text-xs mb-2">✏️ {txt.modification} (2)</h3>
                <div className="space-y-1 text-xs">
                  <div className="flex justify-between"><span className="text-gray-400">count</span><span className="text-white font-mono">{results.modification_count}</span></div>
                </div>
              </div>

              {/* Burst */}
              <div className="bg-cyan-900/20 rounded-xl p-2 border border-cyan-500/30">
                <h3 className="text-cyan-400 font-semibold text-xs mb-2">💥 {txt.burst} (3)</h3>
                <div className="space-y-1 text-xs">
                  <Tooltip id="burst_count"><div className="flex justify-between cursor-help"><span className="text-gray-400">count</span><span className="text-white font-mono">{results.burst_count}</span></div></Tooltip>
                  <div className="flex justify-between"><span className="text-gray-400">segments</span><span className="text-white font-mono">{results.burst_segments}</span></div>
                  <Tooltip id="burst_speed"><div className="flex justify-between cursor-help"><span className="text-gray-400">max_speed</span><span className="text-white font-mono">{results.max_burst_speed}</span></div></Tooltip>
                </div>
              </div>

              {/* Hesitation */}
              <div className="bg-blue-900/20 rounded-xl p-2 border border-blue-500/30">
                <h3 className="text-blue-400 font-semibold text-xs mb-2">🤔 {txt.hesitation} (3)</h3>
                <div className="space-y-1 text-xs">
                  <Tooltip id="hesitation_count"><div className="flex justify-between cursor-help"><span className="text-gray-400">count</span><span className="text-white font-mono">{results.hesitation_count}</span></div></Tooltip>
                  <div className="flex justify-between"><span className="text-gray-400">locations</span><span className="text-white font-mono text-xs">[{results.hesitation_locations.slice(0,3).join(',')}]</span></div>
                </div>
              </div>

              {/* Fluency */}
              <div className="bg-purple-900/20 rounded-xl p-2 border border-purple-500/30">
                <h3 className="text-purple-400 font-semibold text-xs mb-2">🌊 {txt.fluency} (2)</h3>
                <div className="space-y-1 text-xs">
                  <div className="flex justify-between"><span className="text-gray-400">score</span><span className="text-white font-mono">{results.fluency_score}</span></div>
                  <div className="flex justify-between"><span className="text-gray-400">level</span><span className={`font-mono ${getStatusColor(results.fluency_level)} text-white px-1 rounded text-xs`}>{results.fluency_level}</span></div>
                </div>
              </div>

              {/* Pauses */}
              <div className="bg-slate-800/50 rounded-xl p-2 border border-slate-600/30">
                <h3 className="text-slate-300 font-semibold text-xs mb-2">⏸️ {txt.pauses}</h3>
                <div className="space-y-1 text-xs">
                  <Tooltip id="short_pauses"><div className="flex justify-between cursor-help"><span className="text-gray-400">{txt.short} (2-5s)</span><span className="text-white font-mono">{results.pause_pattern.short_pauses}</span></div></Tooltip>
                  <Tooltip id="medium_pauses"><div className="flex justify-between cursor-help"><span className="text-gray-400">{txt.medium} (5-15s)</span><span className="text-white font-mono">{results.pause_pattern.medium_pauses}</span></div></Tooltip>
                  <Tooltip id="long_pauses"><div className="flex justify-between cursor-help"><span className="text-gray-400">{txt.long} (&gt;15s)</span><span className="text-white font-mono">{results.pause_pattern.long_pauses}</span></div></Tooltip>
                </div>
              </div>
            </div>

            {/* Chinese IME Section */}
            {results.detected_language.includes('Chinese') && (
              <div className="mt-3 bg-red-900/20 rounded-xl p-3 border border-red-500/30">
                <h3 className="text-red-400 font-semibold text-xs mb-2">🇨🇳 {txt.chineseIME}</h3>
                <div className="grid grid-cols-3 gap-4 text-xs">
                  <div>
                    <span className="text-gray-400">{txt.imeEvents}: </span>
                    <span className="text-white font-mono">{results.ime_events}</span>
                  </div>
                  <div>
                    <span className="text-gray-400">{txt.keystrokeRatio}: </span>
                    <span className="text-red-300 font-mono font-bold">{results.keystroke_ratio}</span>
                    <span className="text-gray-500 ml-1">({txt.typical}: 3.0-4.0)</span>
                  </div>
                  <div>
                    <span className="text-gray-400">{txt.pinyinCaptured}</span>
                    <span className="text-green-400 ml-1">✅</span>
                  </div>
                </div>
              </div>
            )}

            <div className="mt-3 text-center text-gray-500 text-xs">
              CRPL (Celestelin Rhythm Perception Layer) • 24 Fields • 7 Categories
            </div>
          </div>
        )}

        {/* Instructions */}
        {!results && (
          <div className="bg-white/5 rounded-xl p-3 text-center">
            <p className="text-purple-300 text-sm">{txt.instructions}</p>
          </div>
        )}

        {/* Footer */}
        <div className="mt-4 text-center text-gray-500 text-xs">
          {txt.footer} 💜
        </div>
      </div>
    </div>
  );
};

export default RhythmDetectorPro;
