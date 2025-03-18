// src/types.ts
export interface Reiseplan {
    titel: string;
    startdatum: string;
    enddatum: string;
    reiseziel: string;
    reisende?: string[];
    fluege?: Flug[];
    hotels?: Hotel[];
    aktivitaeten?: Aktivitaet[];
    zusatzinfo?: Zusatzinfo;
  }
  
  export interface Flug {
    airline: string;
    flugNr: string;
    abflugOrt: string;
    abflugCode: string;
    abflugZeit: string;
    ankunftOrt: string;
    ankunftCode: string;
    ankunftZeit: string;
    buchungsNr?: string;
  }
  
  export interface Hotel {
    name: string;
    adresse: string;
    checkin: string;
    checkout: string;
    buchungsNr?: string;
  }
  
  export interface Aktivitaet {
    name: string;
    datum: string;
    startzeit: string;
    endzeit: string;
    ort?: string;
    buchungsNr?: string;
  }
  
  export interface Kontakt {
    name: string;
    telefon: string;
  }
  
  export interface Zusatzinfo {
    notfallkontakte?: Kontakt[];
    waehrung?: string;
    zeitzone?: string;
    notizen?: string;
  }