"use client";
import { useState, useEffect } from "react";

type EditSkeletalPointsProps = {
    nodes: { x: number; y: number }[];
    edges: { node1: number; node2: number }[];
};

enum EditModes {
    Move = "Move",
    Delete = "Delete",
    Add = "Add",
    Connect = "Connect",
}

const EditSkeletalPoints = ({ nodes, edges }: EditSkeletalPointsProps) => {
    const [EditMode, setEditMode] = useState<EditModes|null>(null);
    const [Nodes, setNodes] = useState<{ x: number; y: number }[]>(nodes);
    const [Edges, setEdges] = useState<{ node1: number; node2: number }[]>(edges);
    const [SelectedNodeIndex, setSelectedNodeIndex] = useState<number | null>(null);

    const handleUpload = async () => {
        const payload = {
            nodes: Nodes,
            edges: Edges,
        };

        try {
            const response = await fetch("/api/upload-skeletal-points", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(payload),
            });

            if (response.ok) {
            console.log("Upload successful");
            } else {
            console.error("Upload failed");
            }
        } catch (error) {
            console.error("Error during upload:", error);
        }
    };

    const handleChangeEditMode = (mode: EditModes) => {
        setEditMode((prevMode) => (prevMode === mode ? null : mode));
    }

    useEffect(() => {
        console.log("EditMode changed:", EditMode);
    }, [EditMode]);

    const handleMoveMouseDown = (index: number) => {
        setSelectedNodeIndex(index);
    };

    const handleMoveMouseMove = (event: React.MouseEvent<SVGSVGElement>) => {
        if (SelectedNodeIndex !== null) {
            const svg = event.currentTarget;
            const rect = svg.getBoundingClientRect();
            const x = event.clientX - rect.left;
            const y = event.clientY - rect.top;

            setNodes((prevNodes) =>
                prevNodes.map((node, idx) =>
                    idx === SelectedNodeIndex ? { x, y } : node
                )
            );
        }
    };

    const handleMoveMouseUp = () => {
        setSelectedNodeIndex(null);
    };

    return (
        <div className="w-screen h-auto flex flex-col items-center">
            <div className="">
                <div className="flex flex-row bg-gray-100 p-1 divide-x-2 divide-gray-300">
                    {Object.values(EditModes).map((element) => (
                        <button
                            key={element}
                            className={"px-2 py-1 " + (EditMode === element ? "bg-blue-300 z-10" : "")}
                            onClick={() => handleChangeEditMode(element)}
                        >
                            {element}
                        </button>
                    ))}
                </div>
                <div className="pt-2">
                    <svg
                        className=""
                        onMouseMove={handleMoveMouseMove}
                        onMouseUp={handleMoveMouseUp}
                        width="500"
                        height="500"
                    >
                        {Edges.map((edge, index) => {
                            const node1 = Nodes[edge.node1];
                            const node2 = Nodes[edge.node2];
                            return (
                                <line
                                    key={index}
                                    x1={node1.x}
                                    y1={node1.y}
                                    x2={node2.x}
                                    y2={node2.y}
                                    stroke="yellow"
                                    strokeWidth="2"
                                />
                            );
                        })}
                        {Nodes.map((node, index) => (
                            <circle
                                key={index}
                                cx={node.x}
                                cy={node.y}
                                r="5"
                                fill="red"
                                onMouseDown={() => handleMoveMouseDown(index)}
                            />
                        ))}
                    </svg>
                </div>
            </div>
            <button className="text-sm self-end p-1">送信</button>
        </div>
    );
};

export default EditSkeletalPoints;