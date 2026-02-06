/**
 * Architect Approval System
 * Queue for review before posting
 */

import { SocialPost } from "../platforms/connector";

export interface ApprovalQueue {
  pending: SocialPost[];
  approved: SocialPost[];
  rejected: SocialPost[];
}

export class ApprovalSystem {
  private queue: ApprovalQueue = {
    pending: [],
    approved: [],
    rejected: []
  };

  private autoTrustedThemes = ["day_in_hive", "token_tuesday"];
  private alertThemes = ["partnership", "crisis_response"];

  async submit(post: SocialPost): Promise<boolean> {
    if (this.autoTrustedThemes.includes(post.theme)) {
      post.status = "approved";
      this.queue.approved.push(post);
      console.log(`[Approval] Auto-approved: ${post.id}`);
      return true;
    }

    this.queue.pending.push(post);
    console.log(`[Approval] Queued for review: ${post.id}`);
    return false;
  }

  async approve(postId: string): Promise<void> {
    const post = this.queue.pending.find(p => p.id === postId);
    if (post) {
      post.status = "approved";
      this.queue.approved.push(post);
      this.queue.pending = this.queue.pending.filter(p => p.id !== postId);
      console.log(`[Approval] Architect approved: ${postId}`);
    }
  }

  async reject(postId: string, reason: string): Promise<void> {
    const post = this.queue.pending.find(p => p.id === postId);
    if (post) {
      post.status = "failed";
      this.queue.rejected.push(post);
      this.queue.pending = this.queue.pending.filter(p => p.id !== postId);
      console.log(`[Approval] Rejected: ${postId} - ${reason}`);
    }
  }

  getQueue(): ApprovalQueue {
    return this.queue;
  }
}

export const approvalSystem = new ApprovalSystem();
