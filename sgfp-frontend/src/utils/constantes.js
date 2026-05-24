// Constantes compartidas entre vistas
// Monedas y zonas horarias reutilizables en Perfil, Cuentas y cualquier otra vista

export const monedas = [
  // Europa
  { etiqueta: 'Euro (€) - EUR', valor: 'EUR' },
  { etiqueta: 'Libra esterlina (£) - GBP', valor: 'GBP' },
  { etiqueta: 'Franco suizo (CHF)', valor: 'CHF' },
  { etiqueta: 'Corona sueca (SEK)', valor: 'SEK' },
  { etiqueta: 'Corona noruega (NOK)', valor: 'NOK' },
  { etiqueta: 'Corona danesa (DKK)', valor: 'DKK' },
  { etiqueta: 'Esloti polaco (PLN)', valor: 'PLN' },
  { etiqueta: 'Corona checa (CZK)', valor: 'CZK' },
  { etiqueta: 'Forinto húngaro (HUF)', valor: 'HUF' },
  { etiqueta: 'Leu rumano (RON)', valor: 'RON' },
  // América
  { etiqueta: 'Dólar estadounidense ($) - USD', valor: 'USD' },
  { etiqueta: 'Dólar canadiense (CA$) - CAD', valor: 'CAD' },
  { etiqueta: 'Peso mexicano (MX$) - MXN', valor: 'MXN' },
  { etiqueta: 'Real brasileño (R$) - BRL', valor: 'BRL' },
  { etiqueta: 'Peso argentino ($) - ARS', valor: 'ARS' },
  { etiqueta: 'Peso chileno ($) - CLP', valor: 'CLP' },
  { etiqueta: 'Peso colombiano ($) - COP', valor: 'COP' },
  { etiqueta: 'Sol peruano (S/) - PEN', valor: 'PEN' },
  // Asia
  { etiqueta: 'Yen japonés (¥) - JPY', valor: 'JPY' },
  { etiqueta: 'Yuan chino (¥) - CNY', valor: 'CNY' },
  { etiqueta: 'Won surcoreano (₩) - KRW', valor: 'KRW' },
  { etiqueta: 'Rupia india (₹) - INR', valor: 'INR' },
  { etiqueta: 'Dólar singapurense (S$) - SGD', valor: 'SGD' },
  { etiqueta: 'Dólar de Hong Kong (HK$) - HKD', valor: 'HKD' },
  { etiqueta: 'Baht tailandés (฿) - THB', valor: 'THB' },
  { etiqueta: 'Dírham emiratí (AED)', valor: 'AED' },
  { etiqueta: 'Riyal saudí (SAR)', valor: 'SAR' },
  { etiqueta: 'Lira turca (₺) - TRY', valor: 'TRY' },
  // Oceanía
  { etiqueta: 'Dólar australiano (A$) - AUD', valor: 'AUD' },
  { etiqueta: 'Dólar neozelandés (NZ$) - NZD', valor: 'NZD' },
  // África
  { etiqueta: 'Rand sudafricano (R) - ZAR', valor: 'ZAR' },
  { etiqueta: 'Libra egipcia (EGP)', valor: 'EGP' },
  // Cripto
  { etiqueta: 'Bitcoin (BTC)', valor: 'BTC' },
  { etiqueta: 'Ethereum (ETH)', valor: 'ETH' }
]

export const zonasHorarias = [
  // España
  { etiqueta: 'Atlántico/Canarias (UTC+0/+1)', valor: 'Atlantic/Canary' },
  { etiqueta: 'Europa/Madrid (UTC+1/+2)', valor: 'Europe/Madrid' },
  // Europa
  { etiqueta: 'Europa/Londres (UTC+0/+1)', valor: 'Europe/London' },
  { etiqueta: 'Europa/París (UTC+1/+2)', valor: 'Europe/Paris' },
  { etiqueta: 'Europa/Berlín (UTC+1/+2)', valor: 'Europe/Berlin' },
  { etiqueta: 'Europa/Roma (UTC+1/+2)', valor: 'Europe/Rome' },
  { etiqueta: 'Europa/Lisboa (UTC+0/+1)', valor: 'Europe/Lisbon' },
  { etiqueta: 'Europa/Ámsterdam (UTC+1/+2)', valor: 'Europe/Amsterdam' },
  { etiqueta: 'Europa/Bruselas (UTC+1/+2)', valor: 'Europe/Brussels' },
  { etiqueta: 'Europa/Zúrich (UTC+1/+2)', valor: 'Europe/Zurich' },
  { etiqueta: 'Europa/Estocolmo (UTC+1/+2)', valor: 'Europe/Stockholm' },
  { etiqueta: 'Europa/Oslo (UTC+1/+2)', valor: 'Europe/Oslo' },
  { etiqueta: 'Europa/Copenhague (UTC+1/+2)', valor: 'Europe/Copenhagen' },
  { etiqueta: 'Europa/Helsinki (UTC+2/+3)', valor: 'Europe/Helsinki' },
  { etiqueta: 'Europa/Varsovia (UTC+1/+2)', valor: 'Europe/Warsaw' },
  { etiqueta: 'Europa/Bucarest (UTC+2/+3)', valor: 'Europe/Bucharest' },
  { etiqueta: 'Europa/Atenas (UTC+2/+3)', valor: 'Europe/Athens' },
  { etiqueta: 'Europa/Moscú (UTC+3)', valor: 'Europe/Moscow' },
  // América
  { etiqueta: 'América/Nueva York (UTC-5/-4)', valor: 'America/New_York' },
  { etiqueta: 'América/Chicago (UTC-6/-5)', valor: 'America/Chicago' },
  { etiqueta: 'América/Denver (UTC-7/-6)', valor: 'America/Denver' },
  { etiqueta: 'América/Los Ángeles (UTC-8/-7)', valor: 'America/Los_Angeles' },
  { etiqueta: 'América/Toronto (UTC-5/-4)', valor: 'America/Toronto' },
  { etiqueta: 'América/Ciudad de México (UTC-6/-5)', valor: 'America/Mexico_City' },
  { etiqueta: 'América/São Paulo (UTC-3)', valor: 'America/Sao_Paulo' },
  { etiqueta: 'América/Buenos Aires (UTC-3)', valor: 'America/Argentina/Buenos_Aires' },
  { etiqueta: 'América/Santiago (UTC-4/-3)', valor: 'America/Santiago' },
  { etiqueta: 'América/Bogotá (UTC-5)', valor: 'America/Bogota' },
  { etiqueta: 'América/Lima (UTC-5)', valor: 'America/Lima' },
  // Asia
  { etiqueta: 'Asia/Tokio (UTC+9)', valor: 'Asia/Tokyo' },
  { etiqueta: 'Asia/Shanghái (UTC+8)', valor: 'Asia/Shanghai' },
  { etiqueta: 'Asia/Seúl (UTC+9)', valor: 'Asia/Seoul' },
  { etiqueta: 'Asia/Calcuta (UTC+5:30)', valor: 'Asia/Calcutta' },
  { etiqueta: 'Asia/Singapur (UTC+8)', valor: 'Asia/Singapore' },
  { etiqueta: 'Asia/Dubái (UTC+4)', valor: 'Asia/Dubai' },
  { etiqueta: 'Europa/Estambul (UTC+3)', valor: 'Europe/Istanbul' },
  // Oceanía
  { etiqueta: 'Australia/Sídney (UTC+10/+11)', valor: 'Australia/Sydney' },
  { etiqueta: 'Australia/Melbourne (UTC+10/+11)', valor: 'Australia/Melbourne' },
  { etiqueta: 'Pacífico/Auckland (UTC+12/+13)', valor: 'Pacific/Auckland' },
  // África
  { etiqueta: 'África/Johannesburgo (UTC+2)', valor: 'Africa/Johannesburg' },
  { etiqueta: 'África/El Cairo (UTC+2)', valor: 'Africa/Cairo' },
  { etiqueta: 'África/Lagos (UTC+1)', valor: 'Africa/Lagos' }
]