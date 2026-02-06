/**
 * SofieLabs Content Strategy
 * Weekly themed content across all platforms
 */

export type ContentTheme = 
  | "day_in_hive"
  | "token_tuesday"
  | "wellness_wednesday"
  | "tech_thursday"
  | "future_friday"
  | "system_saturday"
  | "sovereignty_sunday";

export interface ContentPlan {
  theme: ContentTheme;
  day: string;
  platforms: string[];
  postCount: number;
}

export const WEEKLY_STRATEGY: Record<ContentTheme, ContentPlan> = {
  day_in_hive: {
    theme: "day_in_hive",
    day: "Monday",
    platforms: ["twitter", "instagram", "tiktok"],
    postCount: 5
  },
  token_tuesday: {
    theme: "token_tuesday",
    day: "Tuesday",
    platforms: ["twitter", "linkedin", "youtube"],
    postCount: 4
  },
  wellness_wednesday: {
    theme: "wellness_wednesday",
    day: "Wednesday",
    platforms: ["instagram", "tiktok", "youtube"],
    postCount: 5
  },
  tech_thursday: {
    theme: "tech_thursday",
    day: "Thursday",
    platforms: ["twitter", "linkedin", "youtube"],
    postCount: 3
  },
  future_friday: {
    theme: "future_friday",
    day: "Friday",
    platforms: ["twitter", "youtube", "linkedin"],
    postCount: 4
  },
  system_saturday: {
    theme: "system_saturday",
    day: "Saturday",
    platforms: ["instagram", "tiktok", "youtube"],
    postCount: 4
  },
  sovereignty_sunday: {
    theme: "sovereignty_sunday",
    day: "Sunday",
    platforms: ["twitter", "instagram", "youtube"],
    postCount: 3
  }
};

export class ContentStrategy {
  getTodayTheme(): ContentTheme {
    const themes: ContentTheme[] = [
      "sovereignty_sunday",
      "day_in_hive",
      "token_tuesday",
      "wellness_wednesday",
      "tech_thursday",
      "future_friday",
      "system_saturday"
    ];
    return themes[new Date().getDay()];
  }

  getTodaysPlan(): ContentPlan {
    return WEEKLY_STRATEGY[this.getTodayTheme()];
  }

  getHashtags(theme: ContentTheme): string[] {
    const tags: Record<ContentTheme, string[]> = {
      day_in_hive: ["#DayInTheHive", "#SwarmIntelligence"],
      token_tuesday: ["#TokenTuesday", "#MINEtoken"],
      wellness_wednesday: ["#WellnessWednesday", "#Sovereignty"],
      tech_thursday: ["#TechThursday", "#OpenSource"],
      future_friday: ["#FutureFriday", "#Quantum"],
      system_saturday: ["#SystemSaturday", "#Ecosystem"],
      sovereignty_sunday: ["#SovereigntySunday", "#Love"]
    };
    return ["#SofieLabs", "#TerraCare", ...tags[theme]];
  }
}

export const contentStrategy = new ContentStrategy();
