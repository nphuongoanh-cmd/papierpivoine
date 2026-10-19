/**
 * Papier Pivoine · formulaire de contact de papierpivoine.fr/apropos/#ecrire
 *
 * Reçoit les messages du formulaire, les range dans ce Google Sheet (onglet « Messages »)
 * et les envoie par e-mail à Camélia. Répondre à l'e-mail répond directement à la personne.
 *
 * Installation : voir LISEZ-MOI.md, dans le même dossier (ajouts/contact/).
 */

const CONFIG = {
  EMAIL: 'camelia@camelianguyen.fr',   // où arrivent les messages
  ONGLET: 'Messages',                  // nom de l'onglet du Google Sheet
  MAX_PRENOM: 80,
  MAX_EMAIL: 200,
  MAX_MESSAGE: 5000,
  MAX_PAR_HEURE: 5,                    // messages au plus, par adresse e-mail et par heure
};

/** Appelé par le formulaire du site. */
function doPost(e) {
  try {
    const p = (e && e.parameter) || {};

    // Champ piège : invisible pour les gens, rempli seulement par les robots. On fait comme si tout allait bien.
    if (p.site_web) return repondre({ ok: true });

    const prenom = nettoyer(p.prenom, CONFIG.MAX_PRENOM);
    const email = nettoyer(p.email, CONFIG.MAX_EMAIL);
    const message = nettoyer(p.message, CONFIG.MAX_MESSAGE);
    if (!prenom || !message || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      return repondre({ ok: false, erreur: 'champs' });
    }

    // Pas plus de MAX_PAR_HEURE messages par adresse et par heure.
    const cache = CacheService.getScriptCache();
    const cle = 'n_' + email.toLowerCase();
    const n = Number(cache.get(cle) || 0);
    if (n >= CONFIG.MAX_PAR_HEURE) return repondre({ ok: false, erreur: 'trop' });
    cache.put(cle, String(n + 1), 3600);

    onglet().appendRow([new Date(), sansFormule(prenom), sansFormule(email), sansFormule(message)]);

    MailApp.sendEmail({
      to: CONFIG.EMAIL,
      replyTo: email,
      name: 'papierpivoine.fr',
      subject: 'Message de ' + prenom + ' (papierpivoine.fr)',
      body: message + '\n\n— ' + prenom + ' <' + email + '>\n\nRéponds simplement à cet e-mail pour lui écrire.',
    });

    return repondre({ ok: true });
  } catch (err) {
    console.error(err);
    return repondre({ ok: false, erreur: 'serveur' });
  }
}

/** Pour vérifier dans un navigateur que l'application est bien en ligne. */
function doGet() {
  return ContentService.createTextOutput('Formulaire de contact Papier Pivoine : en ligne.');
}

function onglet() {
  const classeur = SpreadsheetApp.getActiveSpreadsheet();
  let feuille = classeur.getSheetByName(CONFIG.ONGLET);
  if (!feuille) feuille = classeur.insertSheet(CONFIG.ONGLET);
  if (feuille.getLastRow() === 0) {
    feuille.appendRow(['Date', 'Prénom', 'E-mail', 'Message']);
    feuille.setFrozenRows(1);
  }
  return feuille;
}

function nettoyer(valeur, max) {
  return String(valeur || '').replace(/\r\n?/g, '\n').trim().slice(0, max);
}

/** Empêche un texte commençant par =, +, - ou @ d'être lu comme une formule par Google Sheets. */
function sansFormule(texte) {
  return /^[=+\-@]/.test(texte) ? "'" + texte : texte;
}

function repondre(objet) {
  return ContentService.createTextOutput(JSON.stringify(objet)).setMimeType(ContentService.MimeType.JSON);
}
