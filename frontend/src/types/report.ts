export type JsonValue =
  | string
  | number
  | boolean
  | null
  | { [key: string]: JsonValue }
  | JsonValue[];

export interface AnalyzeResponse {
  analysis_id: string;
}

export interface AnalysisStatusResponse {
  analysis_id?: string;
  status: string;
  detail?: string;
}

export interface RiskAssessment {
  risk_score: number;
  classification: string;
}

export interface MitreTechnique {
  technique_id: string;
  technique_name: string;
  evidence_count: number;
  [key: string]: JsonValue | undefined;
}

export interface HeuristicFlag {
  type: string;
  severity: string;
  details?: string | string[];
  [key: string]: JsonValue | undefined;
}

export interface ExecutionTimelineEvent {
  pid?: number | string;
  type?: string;
  target?: string;
  timestamp?: string;
  [key: string]: JsonValue | undefined;
}

export interface ProcessTreeNode {
  id?: string | number;
  pid?: string | number;
  name?: string;
  image?: string;
  command_line?: string;
  children?: ProcessTreeNode[];
}

export type ProcessTreeData =
  | ProcessTreeNode[]
  | Record<string, Array<string | number | ProcessTreeNode>>;

export interface MitreAttackAnalysis {
  mapped_techniques: MitreTechnique[];
  technique_count: number;
  technique_summary?: string;
  tactic_distribution: Record<string, number>;
}

export interface AdvancedBehaviorAnalysis {
  process_tree: ProcessTreeData;
  execution_map?: JsonValue;
  execution_timeline: ExecutionTimelineEvent[];
  heuristic_flags: HeuristicFlag[];
}

export interface AnalysisReport {
  analysis_metadata: Record<string, JsonValue | undefined>;
  sample_information: Record<string, JsonValue | undefined>;
  risk_assessment: RiskAssessment;
  behavior_summary?: string | Record<string, JsonValue | undefined>;
  mitre_attack_analysis: MitreAttackAnalysis;
  advanced_behavior_analysis: AdvancedBehaviorAnalysis;
  indicators_of_compromise?: JsonValue;
}
