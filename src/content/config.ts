import { defineCollection, z } from 'astro:content';

const blog = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    pubDate: z.coerce.date(),
    updatedDate: z.coerce.date().optional(),
    category: z.enum(['finance', 'customs', 'ai-tech', 'policy']),
    tags: z.array(z.string()).default([]),
    relatedTool: z.enum(['customs', 'salary', 'dividend', 'ai', 'severance', 'loan']).optional(),
    faq: z.array(z.object({
      q: z.string(),
      a: z.string(),
    })).optional(),
  }),
});

export const collections = { blog };
