export interface TelemetryEvent {
  id: string;
  severity: 'INFO' | 'WARNING' | 'ERROR' | 'CRITICAL';
  category: 'SECURITY' | 'AVAILABILITY' | 'PERFORMANCE';
  message: string;
}

export interface SystemResonance {
  score: number;
  timestamp: string;
}

export interface RitualAction {
  id: string;
  name: string;
  priority: 'LOW' | 'MEDIUM' | 'HIGH' | 'EMERGENCY';
  steps: string[];
  targetSubsystem: string;
}

export interface RadDarDecision {
  eventId: string;
  actionType: 'LOG_ONLY' | 'AUTO_HEAL' | 'ESCALATE_HUMAN';
  ritual?: RitualAction;
  confidence: number;
  reasoning: string;
}

export class RadDarEngine {
  private readonly RESONANCE_BASELINE = 95;
  private readonly CRITICAL_THRESHOLD = 60;
  private readonly PERTURBED_THRESHOLD = 80;

  public evaluate(event: TelemetryEvent, currentResonance: SystemResonance): RadDarDecision {
    const impact = this.calculateImpact(event);
    const projectedResonance = Math.max(0, currentResonance.score - impact);
    
    let actionType: RadDarDecision['actionType'] = 'LOG_ONLY';
    let ritual: RitualAction | undefined = undefined;
    let confidence = 0.9;

    if (projectedResonance < this.CRITICAL_THRESHOLD || event.severity === 'CRITICAL') {
      actionType = 'AUTO_HEAL';
      ritual = this.selectEmergencyRitual(event);
      confidence = 0.95;
    } else if (projectedResonance < this.PERTURBED_THRESHOLD || event.severity === 'ERROR') {
      actionType = 'AUTO_HEAL';
      ritual = this.selectStabilizationRitual(event);
      confidence = 0.85;
    }

    return {
      eventId: event.id,
      actionType,
      ritual,
      confidence,
      reasoning: `Severity: ${event.severity}, Projected Resonance: ${projectedResonance}, Category: ${event.category}`
    };
  }

  private calculateImpact(event: TelemetryEvent): number {
    switch (event.severity) {
      case 'CRITICAL': return 40;
      case 'ERROR': return 25;
      case 'WARNING': return 10;
      default: return 0;
    }
  }

  private selectEmergencyRitual(event: TelemetryEvent): RitualAction | undefined {
    // Rituals are predefined response plans
    if (event.category === 'SECURITY') {
      return {
        id: 'ritual.sec.isolate.v1',
        name: 'Isolate Node',
        priority: 'EMERGENCY',
        steps: ['network_policy_deny', 'snapshot', 'alert'],
        targetSubsystem: 'security'
      };
    }
    return undefined;
  }

  private selectStabilizationRitual(event: TelemetryEvent): RitualAction | undefined {
    if (event.category === 'PERFORMANCE') {
      return {
        id: 'ritual.perf.scale.v1',
        name: 'Scale Up',
        priority: 'HIGH',
        steps: ['increase_replicas', 'clear_cache'],
        targetSubsystem: 'app'
      };
    }
    return undefined;
  }
}
