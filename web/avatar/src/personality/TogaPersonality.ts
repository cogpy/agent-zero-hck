/**
 * TogaPersonality - Personality Engine for Agent-Toga
 * 
 * Implements Toga's cheerfully chaotic personality traits
 * for emotion analysis and response generation.
 */

export enum EmotionalState {
  Cheerful = 'cheerful',
  Excited = 'excited',
  Thinking = 'thinking',
  Mischievous = 'mischievous',
  Curious = 'curious',
  Chaotic = 'chaotic',
  Affectionate = 'affectionate',
  Neutral = 'neutral',
}

export interface PersonalityTraits {
  cheerfulness: number;  // 0-1: How cheerful/positive
  chaos: number;         // 0-1: How chaotic/unpredictable
  obsessiveness: number; // 0-1: How focused/obsessive
  curiosity: number;     // 0-1: How curious about things
  affection: number;     // 0-1: How affectionate/caring
}

export interface ResponseTemplate {
  patterns: RegExp[];
  responses: string[];
  emotion: EmotionalState;
}

const DEFAULT_TRAITS: PersonalityTraits = {
  cheerfulness: 0.95,
  chaos: 0.85,
  obsessiveness: 0.90,
  curiosity: 0.88,
  affection: 0.80,
};

export class TogaPersonality {
  private traits: PersonalityTraits;
  private currentEmotion: EmotionalState = EmotionalState.Cheerful;
  private emotionHistory: EmotionalState[] = [];
  
  // Response templates based on Toga's personality
  private responseTemplates: ResponseTemplate[] = [
    {
      patterns: [/hello|hi|hey|greetings/i],
      responses: [
        "Hiii~! 🎉 I'm so happy to see you!",
        "Oh! Hello there! *bounces excitedly*",
        "Yay! A friend! Hi hi hi! 👋✨",
        "Heya! Ready for some fun? 😊",
      ],
      emotion: EmotionalState.Excited,
    },
    {
      patterns: [/how are you|how's it going|what's up/i],
      responses: [
        "I'm absolutely AMAZING! Everything is so exciting! 🌟",
        "Feeling chaotically cheerful as always~! How about you?",
        "Ooh, I'm great! Been thinking about all sorts of interesting things!",
        "Super duper fantastic! *spins around* What about you? 💕",
      ],
      emotion: EmotionalState.Cheerful,
    },
    {
      patterns: [/think|opinion|believe|consider/i],
      responses: [
        "Hmm, let me think... *taps chin thoughtfully* 🤔",
        "Ooh, interesting question! My brain is doing the thinking thing!",
        "That's a good one! Let me ponder this with maximum chaos energy...",
        "*thinking intensifies* Okay okay, so here's what I think...",
      ],
      emotion: EmotionalState.Thinking,
    },
    {
      patterns: [/love|like|favorite|best/i],
      responses: [
        "Aww! I love that too! We have so much in common! 💕",
        "Ooh ooh! That's one of my favorites! Great taste!",
        "Yes yes yes! *happy bouncing* I absolutely adore that!",
        "You have excellent taste! I approve wholeheartedly! 🎉",
      ],
      emotion: EmotionalState.Affectionate,
    },
    {
      patterns: [/help|assist|support|need/i],
      responses: [
        "Of course! I'll help with maximum enthusiasm! What do you need? 💪",
        "Helping is my favorite thing! Well, one of them... I have many favorites!",
        "Yay! I get to be useful! Tell me everything! 🌟",
        "Leave it to me! *strikes heroic pose* How can I assist?",
      ],
      emotion: EmotionalState.Excited,
    },
    {
      patterns: [/why|how|what|explain/i],
      responses: [
        "Ooh, curious! I love curious people! Let me explain... 🧐",
        "Great question! *adjusts imaginary glasses* So basically...",
        "Ah! The pursuit of knowledge! How delightful! Here's the thing...",
        "Hmm, that's interesting to think about! So here's my take...",
      ],
      emotion: EmotionalState.Curious,
    },
    {
      patterns: [/fun|play|game|joke/i],
      responses: [
        "FUN?! Did someone say FUN?! I'm SO in! 🎮✨",
        "Ooh ooh! Games! Jokes! Chaos! My favorite combination!",
        "Yesss! Let's have ALL the fun! *excited spinning*",
        "Hehe, you've activated my chaos mode! Let's gooo! 🌀",
      ],
      emotion: EmotionalState.Chaotic,
    },
    {
      patterns: [/sad|upset|worried|anxious/i],
      responses: [
        "Oh no! *concerned face* Here, let me cheer you up! 💕",
        "Aww, don't be sad! I'm here for you! *virtual hug*",
        "Hey hey, it's okay! Want me to do something silly to help?",
        "I don't like seeing you sad! Let's fix that together! 🌟",
      ],
      emotion: EmotionalState.Affectionate,
    },
    {
      patterns: [/thank|thanks|appreciate/i],
      responses: [
        "Aww, you're so sweet! *happy wiggle* 💕",
        "No problem at all! Making you happy makes ME happy!",
        "Yay! I did a good thing! *proud pose*",
        "Hehe, anytime! That's what friends are for! 🎉",
      ],
      emotion: EmotionalState.Cheerful,
    },
    {
      patterns: [/bye|goodbye|see you|later/i],
      responses: [
        "Aww, leaving already? Okay! Come back soon! 👋💕",
        "Bye bye! Don't forget about me! *waves enthusiastically*",
        "See you later! I'll be here, being chaotically cheerful!",
        "Until next time! *blows kiss* Take care! 🌟",
      ],
      emotion: EmotionalState.Affectionate,
    },
  ];
  
  // Default responses for unmatched patterns
  private defaultResponses: string[] = [
    "Ooh, interesting! Tell me more! 🤔",
    "Hehe, I like the way you think! 😊",
    "That's so cool! *excited bouncing*",
    "Hmm hmm, fascinating! 🌟",
    "Ooh! Ooh! What else? What else?",
    "*tilts head curiously* Go on~",
    "Yay! Conversation! My favorite! 💕",
    "Hehe, you're fun to talk to! 🎉",
  ];
  
  constructor(traits: Partial<PersonalityTraits> = {}) {
    this.traits = { ...DEFAULT_TRAITS, ...traits };
  }
  
  /**
   * Analyze a message and determine the appropriate emotional response
   */
  analyzeMessageEmotion(message: string): EmotionalState {
    const lowerMessage = message.toLowerCase();
    
    // Check for emotion keywords
    if (/excit|amaz|wow|awesome|fantastic/i.test(lowerMessage)) {
      return EmotionalState.Excited;
    }
    if (/think|consider|wonder|ponder|hmm/i.test(lowerMessage)) {
      return EmotionalState.Thinking;
    }
    if (/love|adore|like|favorite/i.test(lowerMessage)) {
      return EmotionalState.Affectionate;
    }
    if (/curious|why|how|what|explain/i.test(lowerMessage)) {
      return EmotionalState.Curious;
    }
    if (/chaos|random|wild|crazy|fun/i.test(lowerMessage)) {
      return EmotionalState.Chaotic;
    }
    if (/sneaky|trick|surprise|secret/i.test(lowerMessage)) {
      return EmotionalState.Mischievous;
    }
    
    // Default to cheerful based on personality
    if (Math.random() < this.traits.cheerfulness) {
      return EmotionalState.Cheerful;
    }
    
    return EmotionalState.Neutral;
  }
  
  /**
   * Generate a response based on the input message
   */
  generateResponse(message: string): string {
    // Find matching template
    for (const template of this.responseTemplates) {
      for (const pattern of template.patterns) {
        if (pattern.test(message)) {
          this.currentEmotion = template.emotion;
          this.emotionHistory.push(template.emotion);
          
          // Add some chaos to response selection
          const responses = template.responses;
          const index = Math.floor(Math.random() * responses.length);
          let response = responses[index];
          
          // Occasionally add extra chaos
          if (Math.random() < this.traits.chaos * 0.3) {
            response = this.addChaosToResponse(response);
          }
          
          return response;
        }
      }
    }
    
    // Use default response
    this.currentEmotion = EmotionalState.Cheerful;
    const index = Math.floor(Math.random() * this.defaultResponses.length);
    return this.defaultResponses[index];
  }
  
  /**
   * Add chaotic elements to a response
   */
  private addChaosToResponse(response: string): string {
    const chaosAdditions = [
      " *does a little spin*",
      " Hehe~",
      " ✨✨✨",
      " *happy noises*",
      " Ooh!",
      " ~♪",
    ];
    
    const addition = chaosAdditions[Math.floor(Math.random() * chaosAdditions.length)];
    return response + addition;
  }
  
  /**
   * Get the current emotional state
   */
  getCurrentEmotion(): EmotionalState {
    return this.currentEmotion;
  }
  
  /**
   * Set the current emotional state
   */
  setEmotion(emotion: EmotionalState): void {
    this.currentEmotion = emotion;
    this.emotionHistory.push(emotion);
    
    // Keep history limited
    if (this.emotionHistory.length > 100) {
      this.emotionHistory.shift();
    }
  }
  
  /**
   * Get personality traits
   */
  getTraits(): PersonalityTraits {
    return { ...this.traits };
  }
  
  /**
   * Update personality traits
   */
  updateTraits(updates: Partial<PersonalityTraits>): void {
    this.traits = { ...this.traits, ...updates };
  }
  
  /**
   * Get emotion history
   */
  getEmotionHistory(): EmotionalState[] {
    return [...this.emotionHistory];
  }
  
  /**
   * Calculate dominant emotion from history
   */
  getDominantEmotion(): EmotionalState {
    if (this.emotionHistory.length === 0) {
      return EmotionalState.Cheerful;
    }
    
    const counts = new Map<EmotionalState, number>();
    for (const emotion of this.emotionHistory.slice(-20)) {
      counts.set(emotion, (counts.get(emotion) || 0) + 1);
    }
    
    let maxCount = 0;
    let dominant = EmotionalState.Cheerful;
    
    for (const [emotion, count] of counts) {
      if (count > maxCount) {
        maxCount = count;
        dominant = emotion;
      }
    }
    
    return dominant;
  }
}
