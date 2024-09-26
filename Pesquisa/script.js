function search(event) {
    event.preventDefault();

    const allWords = document.getElementById('allWords').value.trim();
    const exactPhrase = document.getElementById('exactPhrase').value.trim();
    const anyWords = document.getElementById('anyWords').value.trim();
    const noneWords = document.getElementById('noneWords').value.trim();

    let query = `site:ufsm.br/pro-reitorias/proplan/`;

    if (allWords) {
        query += ` ${allWords}`;
    }
    if (exactPhrase) {
        query += ` "${exactPhrase}"`;
    }
    if (anyWords) {
        query += ` (${anyWords.split(' ').join(' OR ')})`;
    }
    if (noneWords) {
        query += ` -(${noneWords.split(' ').join(' -')})`;
    }

    const url = `https://www.google.com/search?q=${encodeURIComponent(query)}`;
    window.open(url, '_blank');
}
