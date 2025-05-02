"use client";
import { useState, } from "react";

type EditSkeletalPointsProps = {
    nodes: {x: number, y: number}[];
    edges: {node1: number, node2: number}[];
}

const EditSkeletalPoints = ({
    nodes, 
    edges
}: EditSkeletalPointsProps) => {
    const [Nodes, setNodes] = useState<{x:number, y:number}[]>(nodes);
    const [Edges, setEdges] = useState<{node1:number, node2:number}[]>(edges);

    return (
        <div className="w-screen h-auto flex flex-col items-center">
            <div className="">
                <div className="flex flex-row bg-gray-100 p-1 divide-x-1 divide-gray-300">
                    <button className="text-sm p-1">Move</button>
                    <button className="text-sm p-1">Delete</button>
                    <button className="text-sm p-1">Add</button>
                </div>
                <div className="pt-2">
                    <svg className="">
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
                            />
                        ))}
                    </svg>
                </div>
            </div>
            <button className="text-sm self-end p-1">送信</button>
        </div>
    )
}

export default EditSkeletalPoints;