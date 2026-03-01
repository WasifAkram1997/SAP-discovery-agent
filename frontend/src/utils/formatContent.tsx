import React from 'react';

/**
 * Format message content with basic markdown-like formatting
 */
export const formatContent = (content: string): React.ReactNode => {
  const lines = content.split('\n');
  const elements: React.ReactNode[] = [];
  let currentList: string[] = [];
  let inCodeBlock = false;
  let codeLines: string[] = [];
  let currentTable: string[] = [];

  const flushList = () => {
    if (currentList.length > 0) {
      elements.push(
        <ul key={`list-${elements.length}`} className="list-disc list-inside my-2 space-y-1">
          {currentList.map((item, idx) => (
            <li key={idx}>{formatInline(item)}</li>
          ))}
        </ul>
      );
      currentList = [];
    }
  };

  const flushCodeBlock = () => {
    if (codeLines.length > 0) {
      elements.push(
        <pre key={`code-${elements.length}`} className="bg-gray-100 p-3 rounded-lg overflow-x-auto my-2 text-xs">
          <code>{codeLines.join('\n')}</code>
        </pre>
      );
      codeLines = [];
    }
  };

  const flushTable = () => {
    if (currentTable.length > 1) {
      // Parse table rows
      const rows = currentTable.map(row =>
        row.split('|').map(cell => cell.trim()).filter(cell => cell !== '')
      );

      // Skip separator row (e.g., |---|---|)
      const headerRow = rows[0];
      const dataRows = rows.slice(1).filter(row =>
        !row.every(cell => cell.match(/^[-:]+$/))
      );

      elements.push(
        <div key={`table-${elements.length}`} className="overflow-x-auto my-3">
          <table className="min-w-full border border-gray-300 text-sm">
            <thead className="bg-gray-100">
              <tr>
                {headerRow.map((cell, idx) => (
                  <th key={idx} className="border border-gray-300 px-3 py-2 text-left font-semibold">
                    {formatInline(cell)}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {dataRows.map((row, rowIdx) => (
                <tr key={rowIdx} className={rowIdx % 2 === 0 ? 'bg-white' : 'bg-gray-50'}>
                  {row.map((cell, cellIdx) => (
                    <td key={cellIdx} className="border border-gray-300 px-3 py-2">
                      {formatInline(cell)}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      );
      currentTable = [];
    }
  };

  lines.forEach((line, index) => {
    // Code blocks
    if (line.trim().startsWith('```')) {
      flushTable();
      flushList();
      if (inCodeBlock) {
        flushCodeBlock();
      }
      inCodeBlock = !inCodeBlock;
      return;
    }

    if (inCodeBlock) {
      codeLines.push(line);
      return;
    }

    // Markdown tables (lines with |)
    if (line.includes('|') && line.trim().startsWith('|')) {
      flushList();
      currentTable.push(line);
      return;
    }

    // If we have a table and the line doesn't contain |, flush it
    if (currentTable.length > 0 && !line.includes('|')) {
      flushTable();
    }

    // Bullet points
    if (line.trim().match(/^[-•*]\s/)) {
      flushTable();
      const text = line.trim().replace(/^[-•*]\s/, '');
      currentList.push(text);
      return;
    }

    // Numbered lists
    if (line.trim().match(/^\d+\.\s/)) {
      flushTable();
      flushList();
      const text = line.trim().replace(/^\d+\.\s/, '');
      currentList.push(text);
      return;
    }

    flushList();

    // Headings
    if (line.trim().startsWith('### ')) {
      elements.push(
        <h3 key={index} className="font-semibold text-base mt-3 mb-1">
          {line.replace('### ', '')}
        </h3>
      );
      return;
    }

    if (line.trim().startsWith('## ')) {
      elements.push(
        <h2 key={index} className="font-semibold text-lg mt-3 mb-2">
          {line.replace('## ', '')}
        </h2>
      );
      return;
    }

    if (line.trim().startsWith('# ')) {
      elements.push(
        <h1 key={index} className="font-bold text-xl mt-4 mb-2">
          {line.replace('# ', '')}
        </h1>
      );
      return;
    }

    // Empty lines
    if (line.trim() === '') {
      elements.push(<br key={index} />);
      return;
    }

    // Regular paragraphs
    elements.push(
      <p key={index} className="my-1">
        {formatInline(line)}
      </p>
    );
  });

  flushList();
  flushCodeBlock();
  flushTable();

  return <div className="space-y-0.5">{elements}</div>;
};

/**
 * Format inline elements (bold, italic, code, links)
 */
const formatInline = (text: string): React.ReactNode => {
  const parts: React.ReactNode[] = [];
  let current = '';
  let i = 0;

  while (i < text.length) {
    // Markdown links [text](url)
    if (text[i] === '[') {
      const linkMatch = text.substring(i).match(/^\[([^\]]+)\]\(([^)]+)\)/);
      if (linkMatch) {
        if (current) parts.push(current);
        current = '';
        const linkText = linkMatch[1];
        const linkUrl = linkMatch[2];
        parts.push(
          <a
            key={i}
            href={linkUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-600 hover:text-blue-800 underline"
          >
            {linkText}
          </a>
        );
        i += linkMatch[0].length;
        continue;
      }
    }

    // Bold **text**
    if (text.substr(i, 2) === '**') {
      if (current) parts.push(current);
      current = '';
      i += 2;
      let bold = '';
      while (i < text.length && text.substr(i, 2) !== '**') {
        bold += text[i];
        i++;
      }
      if (text.substr(i, 2) === '**') {
        parts.push(<strong key={i}>{bold}</strong>);
        i += 2;
      } else {
        current = '**' + bold;
      }
      continue;
    }

    // Inline code `text`
    if (text[i] === '`') {
      if (current) parts.push(current);
      current = '';
      i++;
      let code = '';
      while (i < text.length && text[i] !== '`') {
        code += text[i];
        i++;
      }
      if (text[i] === '`') {
        parts.push(
          <code key={i} className="bg-gray-100 px-1.5 py-0.5 rounded text-xs font-mono">
            {code}
          </code>
        );
        i++;
      } else {
        current = '`' + code;
      }
      continue;
    }

    current += text[i];
    i++;
  }

  if (current) parts.push(current);

  return parts.length === 1 ? parts[0] : <>{parts}</>;
};
