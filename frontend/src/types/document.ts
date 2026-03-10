export type DocumentType = 
  | 'licence'
  | 'sro certificate'
  | 'accreditation'
  | 'iso_certificate'
  | 'fstec_license';

export type DocumentStatus = 
  | 'active'
  | 'expiring_soon'
  | 'expired'
  | 'suspended'
  | 'revoked'
  | 'archived';

export interface Document {
  id: number;
  document_number: string;
  document_name: string;
  document_type: DocumentType;
  issuer: string;
  issue_date: string;       
  valid_from: string;
  valid_until: string;
  status: DocumentStatus;
  holder_name: string;
  is_indefinite: boolean;
  description: string | null;
}

export type DocumentCreate = Omit<Document, 'id'>;

export type DocumentUpdate = Partial<Omit<Document, 'id'>>;
