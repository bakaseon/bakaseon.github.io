import { getCollection } from 'astro:content';
import { SITE_CONFIG } from '../config/site';

export async function GET() {
  const posts = await getCollection('blog');
  const baseUrl = SITE_CONFIG.url.replace(/\/$/, '');
  const today = new Date().toISOString().slice(0, 10);

  const staticPages = [
    '',
    '/tools/customs-calculator',
    '/tools/salary-calculator',
    '/tools/severance-calculator',
    '/tools/loan-calculator',
    '/tools/dividend-calculator',
    '/tools/ai-cost-calculator',
    '/blog',
    '/about',
    '/privacy',
    '/terms',
    '/contact',
  ];

  const urls = [
    ...staticPages.map(
      (path) => `
  <url>
    <loc>${baseUrl}${path}/</loc>
    <lastmod>${today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>${path.startsWith('/tools') || path === '' ? '1.0' : '0.8'}</priority>
  </url>`
    ),
    ...posts.map(
      (post) => `
  <url>
    <loc>${baseUrl}/blog/${post.slug}/</loc>
    <lastmod>${post.data.pubDate.toISOString().slice(0, 10)}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.9</priority>
  </url>`
    ),
  ];

  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">${urls.join('')}
</urlset>`;

  return new Response(xml, {
    headers: {
      'Content-Type': 'application/xml; charset=utf-8',
    },
  });
}
