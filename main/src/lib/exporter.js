import jsPDF from 'jspdf';

export const exportToCSV = (elements, tags) => {
  const headers = ['Scene Number', 'Page Number', 'Element Type', 'Text', 'Tags'];
  const rows = elements.map((el) => [
    el.sceneNumber,
    el.pageNumber,
    el.type,
    `"${el.text.replace(/"/g, '""')}"`,
    el.tags?.join(', ') || '',
  ]);

  const csvContent = [
    headers.join(','),
    ...rows.map((row) => row.join(',')),
  ].join('\n');

  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.setAttribute('href', url);
  link.setAttribute('download', 'script_breakdown.csv');
  link.click();
};

export const exportToPDF = async (elements, tags) => {
  const doc = new jsPDF();
  doc.setFont('Courier');
  doc.setFontSize(12);

  let y = 10;
  elements.forEach((el) => {
    if (y > 270) {
      doc.addPage();
      y = 10;
    }
    const tagColor = el.tags?.length && tags[el.tags[0]]?.visible ? tags[el.tags[0]].color : '#000000';
    doc.setTextColor(tagColor);
    doc.text(`${el.sceneNumber}: ${el.text}`, 10, y);
    y += 10;
  });

  doc.save('script_breakdown.pdf');
};