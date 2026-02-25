import type { ProcessTreeData, ProcessTreeNode } from "@/types/report";

interface ProcessTreeProps {
  tree: ProcessTreeData;
}

interface UiProcessNode {
  id: string;
  label: string;
  children: UiProcessNode[];
}

const normalizeFromAdjacency = (
  input: Record<string, Array<string | number | ProcessTreeNode>>,
): UiProcessNode[] => {
  const parentSet = new Set(Object.keys(input));
  const childSet = new Set<string>();

  Object.values(input).forEach((children) => {
    children.forEach((child) => {
      if (typeof child === "string" || typeof child === "number") {
        childSet.add(String(child));
      } else if (child && typeof child === "object") {
        const childId = child.id ?? child.pid;
        if (childId !== undefined) {
          childSet.add(String(childId));
        }
      }
    });
  });

  const build = (nodeId: string): UiProcessNode => {
    const children = (input[nodeId] || []).map((child) => {
      if (typeof child === "string" || typeof child === "number") {
        return build(String(child));
      }

      return normalizeObjectNode(child);
    });

    return {
      id: nodeId,
      label: `PID ${nodeId}`,
      children,
    };
  };

  const roots = [...parentSet].filter((pid) => !childSet.has(pid));
  return (roots.length > 0 ? roots : [...parentSet]).map(build);
};

const normalizeObjectNode = (node: ProcessTreeNode): UiProcessNode => {
  const rawId = node.id ?? node.pid ?? node.name ?? "unknown";
  const id = String(rawId);
  const label = node.name ? `${node.name} (${id})` : `PID ${id}`;

  return {
    id,
    label,
    children: (node.children || []).map(normalizeObjectNode),
  };
};

const toUiNodes = (tree: ProcessTreeData): UiProcessNode[] => {
  if (Array.isArray(tree)) {
    return tree.map(normalizeObjectNode);
  }

  return normalizeFromAdjacency(tree);
};

function TreeBranch({ node, depth }: { node: UiProcessNode; depth: number }) {
  return (
    <li className={depth > 0 ? "ml-4 border-l border-slate-200 pl-4" : ""}>
      <div className="rounded-lg border border-slate-200 bg-slate-50 px-3 py-2 text-sm text-slate-700">
        <span className="font-mono text-xs text-slate-500">{node.id}</span>
        <p className="mt-0.5 font-medium text-slate-800">{node.label}</p>
      </div>
      {node.children.length > 0 && (
        <ul className="mt-2 space-y-2">
          {node.children.map((child) => (
            <TreeBranch key={`${node.id}-${child.id}`} node={child} depth={depth + 1} />
          ))}
        </ul>
      )}
    </li>
  );
}

export default function ProcessTree({ tree }: ProcessTreeProps) {
  const uiNodes = toUiNodes(tree);

  return (
    <section className="rounded-2xl bg-white p-6 shadow-sm">
      <h2 className="mb-4 text-lg font-semibold text-slate-900">
        Process Tree
      </h2>

      {uiNodes.length === 0 ? (
        <p className="rounded-xl border border-slate-200 bg-slate-50 p-4 text-sm text-slate-500">
          No process tree data available.
        </p>
      ) : (
        <ul className="space-y-2">
          {uiNodes.map((node) => (
            <TreeBranch key={node.id} node={node} depth={0} />
          ))}
        </ul>
      )}
    </section>
  );
}
