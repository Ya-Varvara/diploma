import React from 'react';
import { Table } from 'antd';


const convertJSONToMatrix = (json) => {
    const nodes = Object.keys(json.graph_net).map(Number).sort((a, b) => a - b);
    const matrix = Array(nodes.length).fill(null).map(() => Array(nodes.length).fill(''));
  
    nodes.forEach((node) => {
      Object.entries(json.graph_net[node]).forEach(([dest, weight]) => {
        const i = nodes.indexOf(node);
        const j = nodes.indexOf(Number(dest));
        if (i !== -1 && j !== -1) {
          matrix[i][j] = weight;
        }
      });
    });
  
    return matrix;
  };

  const GraphMatrix = ({ json }) => {
    const matrix = convertJSONToMatrix(json);
    const headerBackgroundColor = '#fafafa'; // Цвет фона шапки таблицы по умолчанию в Ant Design
  
    const columns = [{
      title: '',
      dataIndex: 'node',
      key: 'node',
      onCell: () => ({
        style: {
          backgroundColor: headerBackgroundColor,
          fontWeight: 'bold',
        }
      }),
    }]
    .concat(matrix[0].map((_, index) => ({
      title: `x${index + 1}`,
      dataIndex: `x${index + 1}`,
      key: `x${index + 1}`,
    })));
  
    const dataSource = matrix.map((row, index) => ({
      key: `x${index + 1}`,
      node: `x${index + 1}`,
      ...row.reduce((acc, cur, idx) => ({ ...acc, [`x${idx + 1}`]: cur || '' }), {}),
    }));
  
    return <Table columns={columns} dataSource={dataSource} bordered pagination={false} />;
  };

export default GraphMatrix;