import { defineCollection, z } from "astro:content";
import { glob } from "astro/loaders";

const artwork = defineCollection({
  loader: glob({
    pattern: "**/*.md",
    base: "./src/content/artwork",
  }),
  schema: z.object({
    title: z.string(),
    image: z.string(),
    medium: z.string().optional(),
    date: z.string().optional(),
    thumb: z.string().optional(),
    thumbs: z
      .object({
        portrait: z.string().optional(),
        landscape: z.string().optional(),
        square: z.string().optional(),
      })
      .optional(),
    orientation: z.string().optional(),
    size: z.string().optional(),
    price: z.string().optional(),
    status: z.string().optional(),
  }),
});

export const collections = {
  artwork,
};