// src/cli.ts
import { generiereReiseplan } from './main';

async function main(): Promise<void> {
  try {
    const reiseplanPfad = process.argv[2];
    
    if (!reiseplanPfad) {
      console.error('Bitte geben Sie den Pfad zur Reiseplan-JSON-Datei an.');
      console.error('Verwendung: npm run generate -- ./data/reiseplan-london.json');
      process.exit(1);
    }
    
    const ausgabePfad = await generiereReiseplan(reiseplanPfad);
    console.log(`Reiseplan wurde erfolgreich generiert: ${ausgabePfad}`);
  } catch (error) {
    console.error('Fehler beim Generieren des Reiseplans:', error);
    process.exit(1);
  }
}

main();