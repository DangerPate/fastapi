export const statusTranslations: Record<string, string> = {
  active: 'Активен',
  expiring_soon: 'Скоро истекает',
  expired: 'Просрочен',
  suspended: 'Приостановлен',
  revoked: 'Аннулирован',
  archived: 'Архивный'
};

export const statusOptions = [
  { value: 'active', label: 'Активен' },
  { value: 'expiring_soon', label: 'Скоро истекает' },
  { value: 'expired', label: 'Просрочен' },
  { value: 'suspended', label: 'Приостановлен' },
  { value: 'revoked', label: 'Аннулирован' },
  { value: 'archived', label: 'Архивный' }
];