/**
 * SofieLabs Social Media Automation
 * 
 * Multi-platform content automation powered by hive data
 * Twitter/X, Instagram, TikTok, YouTube, LinkedIn
 */

export { ContentStrategy, contentStrategy, WEEKLY_STRATEGY } from "./content/content-strategy";
export { PlatformConnector, platformConnector, PLATFORMS } from "./platforms/connector";
export { VideoGenerator, videoGenerator } from "./video/generator";
export { ContentScheduler, scheduler } from "./scheduler/scheduler";
export { AnalyticsTracker, analytics } from "./analytics/tracker";
export { ApprovalSystem, approvalSystem } from "./approval/system";

import { contentStrategy } from "./content/content-strategy";
import { scheduler } from "./scheduler/scheduler";
import { approvalSystem } from "./approval/system";
import { platformConnector } from "./platforms/connector";
import { videoGenerator } from "./video/generator";
import { analytics } from "./analytics/tracker";

export class SofieLabsSocial {
  async initialize(): Promise<void> {
    console.log("[SofieLabs Social] Initializing...");
    console.log(`[SofieLabs Social] Today's theme: ${contentStrategy.getTodayTheme()}`);
    console.log("[SofieLabs Social] Ready for content generation");
  }

  async generateDailyContent(): Promise<void> {
    await scheduler.run();
    console.log("[SofieLabs Social] Daily content queued for approval");
  }

  async approveAndPost(postId: string): Promise<void> {
    await approvalSystem.approve(postId);
    // Post to platforms
    console.log(`[SofieLabs Social] Posted: ${postId}`);
  }

  async getAnalytics(): Promise<any> {
    return analytics.getDashboard();
  }
}

export const sofieLabsSocial = new SofieLabsSocial();
