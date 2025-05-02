import EditSkeletalPoints from "@/components/EditSkeletalPoints";

const SkeletalPoints = () => {
    const TestNodes = [
        { x: 87, y: 23 },
        { x: 45, y: 78 },
        { x: 6, y: 92 },
        { x: 100, y: 3 },
        { x: 34, y: 66 },
        { x: 12, y: 9 },
        { x: 55, y: 21 },
        { x: 98, y: 100 },
        { x: 0, y: 0 },
        { x: 71, y: 42 },
      ]

    const TestEdges = [
        {node1: 0, node2: 1},
        {node1: 1, node2: 2},
        {node1: 2, node2: 3},
        {node1: 3, node2: 4},
        {node1: 4, node2: 5},
        {node1: 5, node2: 6},
    ]
    return (
        <div>
            <EditSkeletalPoints nodes={TestNodes} edges={TestEdges}/>
        </div>
    )
}

export default SkeletalPoints;